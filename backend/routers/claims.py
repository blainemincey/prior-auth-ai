"""
Claim-level endpoints.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from db import get_db
from services.embedding import embed_document
from data.demo_claims import DEMO_CLAIMS

router = APIRouter(prefix="/api/claims", tags=["claims"])


def _serialize(doc: dict) -> dict:
    """Convert ObjectId and other non-JSON types to strings."""
    out = {}
    for k, v in doc.items():
        if k == "_id":
            out["_id"] = str(v)
        elif isinstance(v, list) and v and isinstance(v[0], float):
            # embedding vector — include dimension count, not full array
            out[k] = f"<vector:{len(v)} dims>"
        else:
            out[k] = v
    return out


def _serialize_full(doc: dict) -> dict:
    """Serialize claim but include full embedding vector."""
    out = {}
    for k, v in doc.items():
        if k == "_id":
            out["_id"] = str(v)
        else:
            out[k] = v
    return out


@router.get("/{scenario}/record")
def get_claim_record(scenario: str):
    """Return the demo claim for the given scenario (A or B)."""
    if scenario not in ("A", "B", "C"):
        raise HTTPException(status_code=400, detail="scenario must be A, B, or C")

    db = get_db()
    claim = db.claims.find_one({"scenario": scenario, "demo_claim": True})
    if not claim:
        raise HTTPException(status_code=404, detail=f"Demo claim for scenario {scenario} not found. Run setup.py first.")

    return _serialize(claim)


@router.post("/{scenario}/embed")
def generate_embedding(scenario: str):
    """
    Generate a Voyage AI embedding for the claim's clinical_notes and
    write it back into the same MongoDB document.
    """
    if scenario not in ("A", "B", "C"):
        raise HTTPException(status_code=400, detail="scenario must be A, B, or C")

    db = get_db()
    claim = db.claims.find_one({"scenario": scenario, "demo_claim": True})
    if not claim:
        raise HTTPException(status_code=404, detail=f"Demo claim for scenario {scenario} not found.")

    clinical_notes = claim.get("clinical_notes", "")
    if not clinical_notes:
        raise HTTPException(status_code=400, detail="Claim has no clinical_notes to embed.")

    existing_embedding = claim.get("clinical_embedding")
    if existing_embedding and isinstance(existing_embedding, list):
        # Embedding already stored — return cached result without calling Voyage AI.
        # The embedding is deterministic (same text → same vector), so re-calling
        # would waste a Voyage API call and risk free-tier rate limits.
        return {
            "status": "ok",
            "claim_id": claim["claim_id"],
            "embedding_model": claim.get("embedding_model", "voyage-3"),
            "embedding_dimensions": len(existing_embedding),
            "embedding_preview": existing_embedding[:8],
            "generated_at": claim.get("embedding_generated_at", ""),
            "message": (
                f"Voyage AI voyage-3 embedding ({len(existing_embedding)} dims) already stored "
                "in this MongoDB document — returned from cache, no API call made."
            ),
        }

    embedding = embed_document(clinical_notes)
    now = datetime.now(timezone.utc).isoformat()

    db.claims.update_one(
        {"scenario": scenario, "demo_claim": True},
        {
            "$set": {
                "clinical_embedding": embedding,
                "embedding_model": "voyage-3",
                "embedding_generated_at": now,
                "updated_at": now,
            }
        },
    )

    return {
        "status": "ok",
        "claim_id": claim["claim_id"],
        "embedding_model": "voyage-3",
        "embedding_dimensions": len(embedding),
        "embedding_preview": embedding[:8],
        "generated_at": now,
        "message": (
            f"Voyage AI voyage-3 embedding ({len(embedding)} dims) written to the "
            "same MongoDB document as the clinical notes. No separate vector store."
        ),
    }


@router.post("/{scenario}/rationale")
def generate_and_writeback_rationale(scenario: str, body: dict):
    """
    Generate a grounded rationale from retrieved context and write it back
    into the original claim document, updating adjudication_status to READY_FOR_REVIEW.
    """
    if scenario not in ("A", "B", "C"):
        raise HTTPException(status_code=400, detail="scenario must be A, B, or C")

    db = get_db()
    claim = db.claims.find_one({"scenario": scenario, "demo_claim": True})
    if not claim:
        raise HTTPException(status_code=404, detail=f"Demo claim for scenario {scenario} not found.")

    policies = body.get("policies", [])
    prior_claims = body.get("prior_claims", [])

    if not policies and not prior_claims:
        raise HTTPException(status_code=400, detail="Must supply retrieved policies and/or prior_claims.")

    from services.rationale import generate_rationale

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    rationale_text = generate_rationale(claim, policies, prior_claims, timestamp)

    # Extract supporting IDs to store as structured fields
    supporting_policy_ids = [p.get("policy_id") for p in policies if p.get("policy_id")]
    comparable_case_ids = [c.get("claim_id") for c in prior_claims if c.get("claim_id")]

    now_iso = now.isoformat()

    db.claims.update_one(
        {"scenario": scenario, "demo_claim": True},
        {
            "$set": {
                "ai_rationale": rationale_text,
                "ai_determination": _extract_recommendation(rationale_text),
                "ai_rationale_generated_at": now_iso,
                "ai_supporting_policies": supporting_policy_ids,
                "ai_comparable_cases": comparable_case_ids,
                "adjudication_status": "READY_FOR_REVIEW",
                "updated_at": now_iso,
            },
            "$push": {
                "status_history": {
                    "status": "READY_FOR_REVIEW",
                    "timestamp": now_iso,
                    "note": "AI-assisted recommendation generated; pending human reviewer attestation.",
                }
            },
        },
    )

    updated_claim = db.claims.find_one({"scenario": scenario, "demo_claim": True})
    return {
        "rationale": rationale_text,
        "determination": _extract_recommendation(rationale_text),
        "supporting_policy_ids": supporting_policy_ids,
        "comparable_case_ids": comparable_case_ids,
        "updated_claim": _serialize(updated_claim),
    }


@router.post("/reset-all")
def soft_reset_all_claims():
    """
    Soft-reset both demo claims (A and B): clear AI output and revert
    adjudication_status to PENDED. Preserves clinical_embedding so Step 2
    returns instantly from cache on the next run without calling Voyage AI.
    """
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()

    reset_fields = {
        "adjudication_status": "PENDED",
        "ai_rationale": None,
        "ai_determination": None,
        "ai_rationale_generated_at": None,
        "ai_supporting_policies": [],
        "ai_comparable_cases": [],
        "status_history": [],
        "updated_at": now,
    }

    db.claims.update_many(
        {"demo_claim": True},
        {"$set": reset_fields},
    )

    results = []
    for scenario in ("A", "B", "C"):
        doc = db.claims.find_one({"scenario": scenario, "demo_claim": True})
        if doc:
            results.append({
                "claim_id": doc["claim_id"],
                "scenario": scenario,
                "embedding_preserved": bool(
                    doc.get("clinical_embedding") and
                    isinstance(doc["clinical_embedding"], list)
                ),
            })

    return {
        "status": "ok",
        "claims_reset": results,
        "message": "Both demo claims reset to PENDED. AI output cleared. Embeddings preserved where present.",
    }


def _extract_recommendation(rationale_text: str) -> str:
    """Pull the Recommendation: line from the rationale."""
    for line in rationale_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Recommendation:"):
            return stripped.replace("Recommendation:", "").strip()
    return "PENDING"
