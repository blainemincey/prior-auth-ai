"""
Vector / hybrid search endpoints.
"""

from fastapi import APIRouter, HTTPException
from db import get_db
from services.vector_search import search_policies, search_prior_claims
from services.hybrid_search import (
    hybrid_search_policies,
    hybrid_search_prior_claims,
)

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("/{scenario}")
def run_vector_search(scenario: str, body: dict):
    """
    Run Atlas Vector Search (or hybrid Vector + Lexical via $rankFusion)
    for the pended claim.

    Body: { filters: {...}, mode: "vector" | "hybrid" }

    Accepts optional MQL filters: plan_type, state, clinical_area,
    adjudication_outcome. Combines semantic relevance with hard filters.
    """
    if scenario not in ("A", "B", "C"):
        raise HTTPException(status_code=400, detail="scenario must be A, B, or C")

    mode = body.get("mode", "vector")
    if mode not in ("vector", "hybrid"):
        raise HTTPException(status_code=400, detail="mode must be 'vector' or 'hybrid'")

    db = get_db()
    claim = db.claims.find_one({"scenario": scenario, "demo_claim": True})
    if not claim:
        raise HTTPException(status_code=404, detail=f"Demo claim for scenario {scenario} not found.")

    embedding = claim.get("clinical_embedding")
    if not embedding or isinstance(embedding, str):
        raise HTTPException(
            status_code=400,
            detail="Claim has no embedding yet. Run /embed first.",
        )

    filters = body.get("filters", {})
    plan_type = filters.get("plan_type") or claim.get("plan_type")
    state = filters.get("state") or claim.get("state")
    clinical_area = filters.get("clinical_area")
    adjudication_outcome = filters.get("adjudication_outcome")

    # Infer clinical area from claim procedure codes if not provided
    if not clinical_area:
        procedure_codes = [p["code"] for p in claim.get("procedure_codes", [])]
        # HCPCS J codes -> specialty biologic infusion
        # HCPCS S codes -> pharmacy/obesity drugs (e.g. S0148 semaglutide)
        # CPT 7xxxx -> diagnostic imaging
        if any(c.startswith("J") for c in procedure_codes):
            clinical_area = "biologic"
        elif any(c.startswith("S") for c in procedure_codes):
            clinical_area = "obesity"
        else:
            clinical_area = "imaging"

    n_policies = filters.get("n_policies", 3)
    n_prior_claims = filters.get("n_prior_claims", 3)

    # Use the stored embedding as the query vector — no extra Voyage API call.
    # The embedding was already generated and stored in Step 2; reusing it here
    # keeps search deterministic and eliminates per-search rate-limit risk.
    query_vector = embedding

    if mode == "hybrid":
        # Lexical side reuses the same clinical_notes that the vector side
        # was built from, so the comparison is apples-to-apples — same input,
        # two retrieval paths fused by $rankFusion.
        query_text = claim.get("clinical_notes", "") or ""

        policy_results, policy_pipeline = hybrid_search_policies(
            db.policies,
            query_vector,
            query_text,
            limit=n_policies,
            clinical_area=clinical_area,
        )

        prior_claim_results, prior_claim_pipeline = hybrid_search_prior_claims(
            db.prior_claims,
            query_vector,
            query_text,
            limit=n_prior_claims,
            plan_type=plan_type,
            state=state,
            clinical_area=clinical_area,
            adjudication_outcome=adjudication_outcome if adjudication_outcome else None,
        )
    else:
        policy_results, policy_pipeline = search_policies(
            db.policies,
            query_vector,
            limit=n_policies,
            plan_type=plan_type,
            clinical_area=clinical_area,
        )

        prior_claim_results, prior_claim_pipeline = search_prior_claims(
            db.prior_claims,
            query_vector,
            limit=n_prior_claims,
            plan_type=plan_type,
            state=state,
            clinical_area=clinical_area,
            adjudication_outcome=adjudication_outcome if adjudication_outcome else None,
        )

    return {
        "mode": mode,
        "query_filters_applied": {
            "plan_type": plan_type,
            "state": state,
            "clinical_area": clinical_area,
            "adjudication_outcome": adjudication_outcome,
        },
        "policies": policy_results,
        "prior_claims": prior_claim_results,
        "pipelines": {
            "policies": policy_pipeline,
            "prior_claims": prior_claim_pipeline,
        },
        "meta": {
            "policy_count": len(policy_results),
            "prior_claim_count": len(prior_claim_results),
            "embedding_model": "voyage-3",
            "search_index_policies": (
                "policy_vector_index + policy_search_index"
                if mode == "hybrid" else "policy_vector_index"
            ),
            "search_index_prior_claims": (
                "prior_claims_vector_index + prior_claims_search_index"
                if mode == "hybrid" else "prior_claims_vector_index"
            ),
        },
    }
