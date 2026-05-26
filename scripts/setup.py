#!/usr/bin/env python3
"""
Healthcare Demo — Setup Script
================================
Idempotent: safe to run multiple times.

What this does (in order):
  1. Connect to Atlas and create the database / collections.
  2. Drop and recreate demo claims (so re-runs are clean).
  3. Create Atlas Vector Search indexes via the MongoDB driver.
  4. Seed coverage policies with Voyage AI embeddings.
  5. Seed prior adjudicated claims with Voyage AI embeddings.
  6. Insert the two demo claims (A, B) with Voyage AI embeddings.
  7. Wait for all Vector Search indexes to reach READY state.
  8. Run a quick smoke-test search against each index.

Usage:
  cd /path/to/healthcaredemo
  python scripts/setup.py

Prerequisites:
  .env file with MONGODB_URI and VOYAGE_API_KEY
"""

import sys
import os
import time

# Allow importing from backend/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from config import settings
from services.embedding import embed_batch, embed_document, embed_query
from data.demo_claims import DEMO_CLAIMS
from data.policies import POLICIES
from data.prior_claims import PRIOR_CLAIMS


# ─────────────────────────────────────────────────────────────────────────────
# Index definitions
# ─────────────────────────────────────────────────────────────────────────────

POLICY_INDEX = SearchIndexModel(
    name="policy_vector_index",
    type="vectorSearch",
    definition={
        "fields": [
            {
                "type": "vector",
                "path": "clinical_embedding",
                "numDimensions": 1024,
                "similarity": "cosine",
            },
            {"type": "filter", "path": "clinical_area"},
            {"type": "filter", "path": "subcategory"},
        ]
    },
)

PRIOR_CLAIMS_INDEX = SearchIndexModel(
    name="prior_claims_vector_index",
    type="vectorSearch",
    definition={
        "fields": [
            {
                "type": "vector",
                "path": "clinical_embedding",
                "numDimensions": 1024,
                "similarity": "cosine",
            },
            {"type": "filter", "path": "plan_type"},
            {"type": "filter", "path": "state"},
            {"type": "filter", "path": "clinical_area"},
            {"type": "filter", "path": "adjudication_outcome"},
        ]
    },
)

CLAIMS_INDEX = SearchIndexModel(
    name="claims_vector_index",
    type="vectorSearch",
    definition={
        "fields": [
            {
                "type": "vector",
                "path": "clinical_embedding",
                "numDimensions": 1024,
                "similarity": "cosine",
            },
            {"type": "filter", "path": "plan_type"},
            {"type": "filter", "path": "state"},
            {"type": "filter", "path": "adjudication_status"},
            {"type": "filter", "path": "scenario"},
        ]
    },
)


# ─── Atlas Search (text) indexes — paired with the vector indexes above
# so $rankFusion can combine semantic + lexical pipelines on the same
# collections, using the same hard-filter fields. `string` fields are
# tokenized for free-text matching; `token` fields are kept verbatim for
# exact-match filtering inside $search.compound.filter clauses.

POLICY_SEARCH_INDEX = SearchIndexModel(
    name="policy_search_index",
    type="search",
    definition={
        "mappings": {
            "dynamic": False,
            "fields": {
                "title": {"type": "string"},
                "criteria_text": {"type": "string"},
                "subcategory": {"type": "string"},
                "clinical_area": {"type": "token"},
            }
        }
    },
)

PRIOR_CLAIMS_SEARCH_INDEX = SearchIndexModel(
    name="prior_claims_search_index",
    type="search",
    definition={
        "mappings": {
            "dynamic": False,
            "fields": {
                "primary_diagnosis_description": {"type": "string"},
                "outcome_rationale": {"type": "string"},
                "clinical_note": {"type": "string"},
                "plan_type": {"type": "token"},
                "state": {"type": "token"},
                "clinical_area": {"type": "token"},
                "adjudication_outcome": {"type": "token"},
                "procedure_codes": {
                    "type": "document",
                    "fields": {
                        "code": {"type": "token"},
                        "description": {"type": "string"},
                    },
                },
            }
        }
    },
)


def log(msg: str) -> None:
    print(f"  {msg}")


def step(msg: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {msg}")
    print(f"{'─' * 60}")


def ensure_index(collection, index_model: SearchIndexModel) -> None:
    """Create index if it doesn't already exist."""
    existing = {idx["name"]: idx for idx in collection.list_search_indexes()}
    name = index_model.document["name"]
    if name in existing:
        log(f"Index '{name}' already exists — skipping creation.")
    else:
        collection.create_search_index(index_model)
        log(f"Index '{name}' creation submitted.")


def wait_for_indexes(collection, index_names: list[str], timeout: int = 300) -> None:
    """Poll until all named indexes reach READY status."""
    log(f"Waiting for indexes to become READY (timeout {timeout}s)...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        statuses = {
            idx["name"]: idx.get("status", "UNKNOWN")
            for idx in collection.list_search_indexes()
        }
        pending = [n for n in index_names if statuses.get(n) != "READY"]
        if not pending:
            log("All indexes READY.")
            return
        log(f"  Pending: {pending} — sleeping 10s...")
        time.sleep(10)
    raise TimeoutError(f"Indexes not READY after {timeout}s: {pending}")


def embed_records(records: list[dict], text_field: str, batch_size: int = 64) -> list[dict]:
    """
    Add Voyage AI embeddings to a list of records.

    Processes in batches with a 1-second pause between batches to stay
    within Voyage AI free-tier rate limits (requests/minute).
    """
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    all_embeddings: list = []

    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        texts = [r[text_field] for r in batch]
        log(f"  Embedding batch {i // batch_size + 1} ({len(texts)} docs)...")
        embeddings = embed_batch(texts, input_type="document")
        all_embeddings.extend(embeddings)
        if i + batch_size < len(records):
            time.sleep(1)  # brief pause between batches — avoids free-tier 429s

    for rec, emb in zip(records, all_embeddings):
        rec["clinical_embedding"] = emb
        rec["embedding_generated_at"] = now
    return records


def main() -> None:
    print("\n" + "=" * 60)
    print("  Healthcare Demo — Atlas Setup")
    print("=" * 60)

    # ── Connect ──────────────────────────────────────────────────
    step("Step 1: Connecting to MongoDB Atlas")
    client = MongoClient(settings.mongodb_uri)
    db = client[settings.db_name]
    log(f"Connected. Database: {settings.db_name}")
    # Quick connectivity check
    db.command("ping")
    log("Ping OK.")

    # ── Collections ──────────────────────────────────────────────
    step("Step 2: Ensuring collections exist")
    for cname in ("claims", "policies", "prior_claims"):
        if cname not in db.list_collection_names():
            db.create_collection(cname)
            log(f"Created collection: {cname}")
        else:
            log(f"Collection '{cname}' already exists.")

    # ── Vector Search Indexes ─────────────────────────────────────
    step("Step 3: Creating Atlas Vector + Search indexes")
    ensure_index(db.policies, POLICY_INDEX)
    ensure_index(db.prior_claims, PRIOR_CLAIMS_INDEX)
    ensure_index(db.claims, CLAIMS_INDEX)
    ensure_index(db.policies, POLICY_SEARCH_INDEX)
    ensure_index(db.prior_claims, PRIOR_CLAIMS_SEARCH_INDEX)

    # ── Seed Policies ─────────────────────────────────────────────
    step("Step 4: Seeding coverage policies with Voyage AI embeddings")
    existing_policy_ids = {
        d["policy_id"] for d in db.policies.find({}, {"policy_id": 1})
    }
    new_policies = [p for p in POLICIES if p["policy_id"] not in existing_policy_ids]

    if new_policies:
        log(f"Embedding {len(new_policies)} new policies via Voyage AI...")
        new_policies = embed_records(new_policies, "criteria_text")
        db.policies.insert_many(new_policies)
        log(f"Inserted {len(new_policies)} policies.")
    else:
        log(f"All {len(POLICIES)} policies already present — skipping.")

    total_policies = db.policies.count_documents({})
    log(f"Total policies in collection: {total_policies}")

    # ── Seed Prior Claims ─────────────────────────────────────────
    step("Step 5: Seeding prior adjudicated claims with Voyage AI embeddings")
    existing_claim_ids = {
        d["claim_id"] for d in db.prior_claims.find({}, {"claim_id": 1})
    }
    new_prior = [c for c in PRIOR_CLAIMS if c["claim_id"] not in existing_claim_ids]

    if new_prior:
        log(f"Embedding {len(new_prior)} new prior claims via Voyage AI...")
        new_prior = embed_records(new_prior, "clinical_note")
        db.prior_claims.insert_many(new_prior)
        log(f"Inserted {len(new_prior)} prior claims.")
    else:
        log(f"All {len(PRIOR_CLAIMS)} prior claims already present — skipping.")

    total_prior = db.prior_claims.count_documents({})
    log(f"Total prior claims in collection: {total_prior}")

    # ── Insert/Refresh Demo Claims ────────────────────────────────
    step("Step 6: Inserting demo claims (A and B) with Voyage AI embeddings")
    for scenario_key, claim in DEMO_CLAIMS.items():
        # Always refresh demo claims so they start in PENDED state
        db.claims.delete_one({"scenario": scenario_key, "demo_claim": True})
        claim_copy = dict(claim)
        log(f"Embedding Scenario {scenario_key} demo claim...")
        embedding = embed_document(claim_copy["clinical_notes"])
        import datetime
        claim_copy["clinical_embedding"] = embedding
        claim_copy["embedding_generated_at"] = datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
        db.claims.insert_one(claim_copy)
        log(
            f"  Scenario {scenario_key}: {claim_copy['claim_id']} inserted "
            f"({len(embedding)}-dim embedding)."
        )

    # ── Wait for Indexes ──────────────────────────────────────────
    step("Step 7: Waiting for Atlas Vector + Search indexes to be READY")
    # Policies and prior_claims are most critical for the demo search
    wait_for_indexes(db.policies, ["policy_vector_index", "policy_search_index"])
    wait_for_indexes(db.prior_claims, ["prior_claims_vector_index", "prior_claims_search_index"])
    log("Claims index may still be building — that's OK; demo uses policies and prior_claims indexes.")

    # ── Smoke Test ────────────────────────────────────────────────
    step("Step 8: Smoke-testing vector search")

    test_query = (
        "lumbar spine MRI radiculopathy disc herniation physical therapy conservative treatment"
    )
    log(f"Query: '{test_query[:60]}...'")
    test_vector = embed_query(test_query)

    policy_results = list(
        db.policies.aggregate([
            {
                "$vectorSearch": {
                    "index": "policy_vector_index",
                    "path": "clinical_embedding",
                    "queryVector": test_vector,
                    "numCandidates": 20,
                    "limit": 3,
                    "filter": {"clinical_area": {"$eq": "imaging"}},
                }
            },
            {"$project": {"policy_id": 1, "title": 1, "_id": 0,
                          "score": {"$meta": "vectorSearchScore"}}},
        ])
    )
    log("Top imaging policy matches:")
    for p in policy_results:
        log(f"  {p['policy_id']} | {p['title'][:50]} | score={p.get('score', 'n/a'):.4f}")

    test_query_b = (
        "rheumatoid arthritis biologic infliximab step therapy methotrexate failed DAS28"
    )
    log(f"Query: '{test_query_b[:60]}...'")
    test_vector_b = embed_query(test_query_b)

    prior_results = list(
        db.prior_claims.aggregate([
            {
                "$vectorSearch": {
                    "index": "prior_claims_vector_index",
                    "path": "clinical_embedding",
                    "queryVector": test_vector_b,
                    "numCandidates": 30,
                    "limit": 3,
                    "filter": {
                        "plan_type": {"$eq": "PPO"},
                        "clinical_area": {"$eq": "biologic"},
                    },
                }
            },
            {"$project": {"claim_id": 1, "adjudication_outcome": 1, "_id": 0,
                          "score": {"$meta": "vectorSearchScore"}}},
        ])
    )
    log("Top biologic prior claim matches:")
    for c in prior_results:
        log(f"  {c['claim_id']} | {c['adjudication_outcome']} | score={c.get('score', 'n/a'):.4f}")

    # ── Done ──────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  Setup complete. Demo is ready to run.")
    print("=" * 60)
    print()
    print("  EXPECTED TOP MATCHES (verify against smoke test above):")
    print("  Scenario A — MRI lumbar: POL-MRI-LUMBAR-2024-03 should be #1 or #2")
    print("  Scenario B — Biologic:   PCL-2024-BIO-2244 or PCL-2024-BIO-1891 should surface")
    print()
    print("  To start the demo:")
    print("    ./start.sh")
    print()


if __name__ == "__main__":
    main()
