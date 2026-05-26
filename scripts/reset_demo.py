#!/usr/bin/env python3
"""
Reset all demo claims between demo runs.

Default (soft) reset — keeps the Voyage AI embedding, clears only the
AI output and status fields. The Step 2 embed button will detect the
existing embedding and skip the Voyage API call, eliminating rate-limit
risk on repeat runs while the UI experience remains identical.

Hard reset (--hard) — clears everything including the embedding. Use
this when you want a true first-run experience or to force a fresh
Voyage API call in Step 2.

Usage:
  python scripts/reset_demo.py           # soft reset (default)
  python scripts/reset_demo.py --hard    # full reset including embedding
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from db import get_db

CLAIMS = ["CLM-2025-0001847", "CLM-2025-0003291", "CLM-2025-0007734"]

# Always cleared — AI output and adjudication state
SOFT_RESET_FIELDS = {
    "adjudication_status": "PENDED",
    "ai_rationale": None,
    "ai_determination": None,
    "ai_rationale_generated_at": None,
    "ai_supporting_policies": [],
    "ai_comparable_cases": [],
    "status_history": [],
}

# Additionally cleared on --hard
HARD_ONLY_FIELDS = {
    "clinical_embedding": None,
    "embedding_model": None,
    "embedding_generated_at": None,
}


def main():
    hard = "--hard" in sys.argv

    reset_fields = dict(SOFT_RESET_FIELDS)
    if hard:
        reset_fields.update(HARD_ONLY_FIELDS)

    mode = "hard (embedding cleared)" if hard else "soft (embedding preserved)"
    print(f"Resetting demo claims [{mode}]...")

    db = get_db()
    for cid in CLAIMS:
        result = db.claims.update_one({"claim_id": cid}, {"$set": reset_fields})
        status = "reset" if result.modified_count else "already clean"
        print(f"  {cid}: {status}")

    if hard:
        print("Done — all claims are PENDED with no embedding or rationale.")
    else:
        print("Done — all claims are PENDED. Embeddings preserved; rationale cleared.")


if __name__ == "__main__":
    main()
