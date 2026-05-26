#!/usr/bin/env python3
"""
Verify the Atlas cluster supports $rankFusion before building hybrid search.

Read-only:
  - Prints the MongoDB server version
  - Runs a tiny $rankFusion query against the existing policy_vector_index
    (two $vectorSearch sub-pipelines with different filters) to exercise
    the stage parser without creating any new indexes

Exit code 0 = supported, non-zero = not supported.
"""
import os
import sys

# Backend modules live one directory up
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from config import settings  # noqa: E402
from pymongo import MongoClient  # noqa: E402
from pymongo.errors import OperationFailure  # noqa: E402


# ─── Configuration ──────────────────────────────────────────────────────
MIN_VERSION = (8, 1)
SMOKE_INDEX = "policy_vector_index"
SMOKE_COLLECTION = "policies"


def main() -> int:
    print("Connecting to Atlas...")
    client = MongoClient(settings.mongodb_uri)
    db = client[settings.db_name]

    # 1) Server version
    info = client.admin.command("buildInfo")
    version = info.get("version", "unknown")
    print(f"  MongoDB server version: {version}")

    parts = version.split(".")
    try:
        major, minor = int(parts[0]), int(parts[1])
        if (major, minor) < MIN_VERSION:
            print(f"  ✗ $rankFusion requires MongoDB {MIN_VERSION[0]}.{MIN_VERSION[1]}+ "
                  f"(cluster is {version}).")
            return 1
        print(f"  ✓ Server version meets $rankFusion requirement "
              f"(>= {MIN_VERSION[0]}.{MIN_VERSION[1]}).")
    except (IndexError, ValueError):
        print(f"  ! Could not parse version '{version}' — continuing with smoke test.")

    # 2) Need an embedded policy to use as a query vector
    sample = db[SMOKE_COLLECTION].find_one(
        {"clinical_embedding": {"$ne": None, "$type": "array"}}
    )
    if not sample:
        print(f"  ✗ No embedded documents in '{SMOKE_COLLECTION}' — run setup.py first.")
        return 1
    qvec = sample["clinical_embedding"]
    print(f"  Using sample document {sample.get('policy_id')!r} as query vector.")

    # 3) $rankFusion smoke test — two $vectorSearch sub-pipelines with different filters
    pipeline = [
        {
            "$rankFusion": {
                "input": {
                    "pipelines": {
                        "vector_all": [
                            {
                                "$vectorSearch": {
                                    "index": SMOKE_INDEX,
                                    "path": "clinical_embedding",
                                    "queryVector": qvec,
                                    "numCandidates": 20,
                                    "limit": 5,
                                }
                            }
                        ],
                        "vector_imaging": [
                            {
                                "$vectorSearch": {
                                    "index": SMOKE_INDEX,
                                    "path": "clinical_embedding",
                                    "queryVector": qvec,
                                    "numCandidates": 20,
                                    "limit": 5,
                                    "filter": {"clinical_area": {"$eq": "imaging"}},
                                }
                            }
                        ],
                    }
                },
                "combination": {
                    "weights": {"vector_all": 1, "vector_imaging": 1}
                },
            }
        },
        {"$limit": 3},
        {"$project": {"_id": 0, "policy_id": 1, "title": 1, "clinical_area": 1}},
    ]

    try:
        results = list(db[SMOKE_COLLECTION].aggregate(pipeline))
    except OperationFailure as e:
        print(f"  ✗ $rankFusion aggregation failed: {e}")
        return 1

    print(f"  ✓ $rankFusion executed successfully — {len(results)} fused result(s).")
    for r in results:
        print(f"    {r.get('policy_id','?'):<32} "
              f"[{r.get('clinical_area','?')}] "
              f"{r.get('title','')}")

    print("\n✓ Cluster supports $rankFusion. Ready to proceed with Phase 1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
