#!/usr/bin/env python3
"""
End-to-end smoke test for the hybrid-search pipeline:

  1. Plain $search against policy_search_index — confirms text index is healthy
  2. Plain $search against prior_claims_search_index — same
  3. $rankFusion combining $vectorSearch + $search on policies — confirms the
     hybrid path we'll wire into the backend in Phase 2

Read-only — no writes. Exit code 0 = all checks passed.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from config import settings  # noqa: E402
from pymongo import MongoClient  # noqa: E402
from pymongo.errors import OperationFailure  # noqa: E402


POLICY_VECTOR_INDEX = "policy_vector_index"
POLICY_SEARCH_INDEX = "policy_search_index"
PRIOR_CLAIMS_SEARCH_INDEX = "prior_claims_search_index"


def section(title: str) -> None:
    print(f"\n── {title} " + "─" * (74 - len(title)))


def main() -> int:
    client = MongoClient(settings.mongodb_uri)
    db = client[settings.db_name]

    # ── 1) Plain $search on policies ──────────────────────────────────
    section("1) $search on policies — text-only")
    pipeline = [
        {
            "$search": {
                "index": POLICY_SEARCH_INDEX,
                "compound": {
                    "must": [
                        {
                            "text": {
                                "query": "lumbar spine MRI radiculopathy",
                                "path": ["title", "criteria_text", "subcategory"],
                            }
                        }
                    ],
                    "filter": [
                        {"equals": {"path": "clinical_area", "value": "imaging"}}
                    ],
                },
            }
        },
        {"$limit": 3},
        {
            "$project": {
                "_id": 0,
                "policy_id": 1,
                "title": 1,
                "clinical_area": 1,
                "text_score": {"$meta": "searchScore"},
            }
        },
    ]
    try:
        results = list(db.policies.aggregate(pipeline))
    except OperationFailure as e:
        print(f"  ✗ $search on policies failed: {e}")
        return 1
    if not results:
        print("  ✗ $search returned 0 results — index may be empty or analyzer issue.")
        return 1
    for r in results:
        print(f"    {r['policy_id']:<32} [{r['clinical_area']}] "
              f"score={r['text_score']:.3f}  {r['title']}")

    # ── 2) Plain $search on prior_claims ──────────────────────────────
    section("2) $search on prior_claims — text-only, with token filter")
    pipeline = [
        {
            "$search": {
                "index": PRIOR_CLAIMS_SEARCH_INDEX,
                "compound": {
                    "must": [
                        {
                            "text": {
                                "query": "infliximab step therapy rheumatoid",
                                "path": ["clinical_note", "outcome_rationale",
                                         "primary_diagnosis_description"],
                            }
                        }
                    ],
                    "filter": [
                        {"equals": {"path": "plan_type", "value": "PPO"}},
                        {"equals": {"path": "clinical_area", "value": "biologic"}},
                    ],
                },
            }
        },
        {"$limit": 3},
        {
            "$project": {
                "_id": 0,
                "claim_id": 1,
                "plan_type": 1,
                "state": 1,
                "adjudication_outcome": 1,
                "text_score": {"$meta": "searchScore"},
            }
        },
    ]
    try:
        results = list(db.prior_claims.aggregate(pipeline))
    except OperationFailure as e:
        print(f"  ✗ $search on prior_claims failed: {e}")
        return 1
    if not results:
        print("  ✗ $search returned 0 results — index may be empty or filter mismatch.")
        return 1
    for r in results:
        print(f"    {r['claim_id']:<24} {r['plan_type']}/{r['state']:<3} "
              f"{r['adjudication_outcome']:<10} score={r['text_score']:.3f}")

    # ── 3) $rankFusion: $vectorSearch + $search on policies ───────────
    section("3) $rankFusion(vector + lexical) on policies")
    sample = db.policies.find_one(
        {"clinical_embedding": {"$ne": None, "$type": "array"}}
    )
    if not sample:
        print("  ✗ No embedded policy found — cannot build query vector.")
        return 1
    qvec = sample["clinical_embedding"]
    print(f"  Query vector from {sample['policy_id']!r}; "
          f"text query: 'lumbar MRI medical necessity criteria'")

    pipeline = [
        {
            "$rankFusion": {
                "input": {
                    "pipelines": {
                        "vector": [
                            {
                                "$vectorSearch": {
                                    "index": POLICY_VECTOR_INDEX,
                                    "path": "clinical_embedding",
                                    "queryVector": qvec,
                                    "numCandidates": 80,
                                    "limit": 10,
                                    "filter": {
                                        "clinical_area": {"$eq": "imaging"}
                                    },
                                }
                            }
                        ],
                        "lexical": [
                            {
                                "$search": {
                                    "index": POLICY_SEARCH_INDEX,
                                    "compound": {
                                        "must": [
                                            {
                                                "text": {
                                                    "query": "lumbar MRI medical necessity criteria",
                                                    "path": ["title", "criteria_text",
                                                             "subcategory"],
                                                }
                                            }
                                        ],
                                        "filter": [
                                            {"equals": {"path": "clinical_area",
                                                        "value": "imaging"}}
                                        ],
                                    },
                                }
                            },
                            {"$limit": 10},
                        ],
                    }
                },
                "combination": {"weights": {"vector": 1, "lexical": 1}},
                "scoreDetails": True,
            }
        },
        {"$limit": 5},
        {
            "$project": {
                "_id": 0,
                "policy_id": 1,
                "title": 1,
                "fused_score": {"$meta": "scoreDetails"},
            }
        },
    ]
    try:
        results = list(db.policies.aggregate(pipeline))
    except OperationFailure as e:
        print(f"  ✗ $rankFusion failed: {e}")
        return 1
    if not results:
        print("  ✗ $rankFusion returned 0 results.")
        return 1
    for r in results:
        details = r.get("fused_score") or {}
        # scoreDetails returns nested rank info per input pipeline
        inputs = details.get("details", [])
        rank_summary = " | ".join(
            f"{d.get('inputPipelineName','?')}: rank={d.get('rank','?')}"
            for d in inputs
        )
        print(f"    {r['policy_id']:<32} {rank_summary}")
        print(f"      {r['title']}")

    print("\n✓ All hybrid-search checks passed. Phase 1 done — ready for Phase 2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
