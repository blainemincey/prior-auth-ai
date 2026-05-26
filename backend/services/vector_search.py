"""
Atlas Vector Search queries.

Uses the $vectorSearch aggregation stage with optional MQL pre-filters.
Filters enforce hard operational constraints (plan_type, state, etc.)
on top of semantic similarity — not unguarded semantic search.
"""

from copy import deepcopy
from typing import Optional, List, Tuple
from pymongo.collection import Collection


POLICIES_INDEX = "policy_vector_index"
PRIOR_CLAIMS_INDEX = "prior_claims_vector_index"

# Number of candidates Atlas Vector Search will consider before returning limit
NUM_CANDIDATES = 80


def _displayable_pipeline(pipeline: List[dict]) -> List[dict]:
    """
    Return a copy of the pipeline with the 1024-element queryVector replaced
    by a short placeholder string, so the pipeline is readable when shown
    to engineers in the UI without dumping thousands of floats.
    """
    redacted = deepcopy(pipeline)
    for stage in redacted:
        vs = stage.get("$vectorSearch")
        if vs and "queryVector" in vs:
            dims = len(vs["queryVector"]) if isinstance(vs["queryVector"], list) else "?"
            vs["queryVector"] = f"<{dims}-dim embedding from step 2>"
    return redacted


def search_policies(
    collection: Collection,
    query_vector: List[float],
    limit: int = 3,
    plan_type: Optional[str] = None,
    clinical_area: Optional[str] = None,
) -> Tuple[List[dict], List[dict]]:
    """
    Search the policies collection by semantic similarity.
    Optional pre-filters on plan_applicability / clinical_area.

    Returns (results, displayable_pipeline).
    """
    vector_search_stage: dict = {
        "index": POLICIES_INDEX,
        "path": "clinical_embedding",
        "queryVector": query_vector,
        "numCandidates": NUM_CANDIDATES,
        "limit": limit,
    }

    filter_clauses = {}
    if clinical_area:
        filter_clauses["clinical_area"] = {"$eq": clinical_area}

    if filter_clauses:
        vector_search_stage["filter"] = filter_clauses

    pipeline = [
        {"$vectorSearch": vector_search_stage},
        {
            "$project": {
                "_id": 0,
                "policy_id": 1,
                "title": 1,
                "clinical_area": 1,
                "subcategory": 1,
                "plan_applicability": 1,
                "cpt_codes": 1,
                "hcpcs_codes": 1,
                "criteria_text": 1,
                "vector_score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    results = list(collection.aggregate(pipeline))
    return results, _displayable_pipeline(pipeline)


def search_prior_claims(
    collection: Collection,
    query_vector: List[float],
    limit: int = 3,
    plan_type: Optional[str] = None,
    state: Optional[str] = None,
    clinical_area: Optional[str] = None,
    adjudication_outcome: Optional[str] = None,
) -> Tuple[List[dict], List[dict]]:
    """
    Search the prior_claims collection by semantic similarity with metadata filters.
    Filters combine semantic relevance with hard operational constraints.

    Returns (results, displayable_pipeline).
    """
    vector_search_stage: dict = {
        "index": PRIOR_CLAIMS_INDEX,
        "path": "clinical_embedding",
        "queryVector": query_vector,
        "numCandidates": NUM_CANDIDATES,
        "limit": limit,
    }

    filter_clauses = {}
    if plan_type:
        filter_clauses["plan_type"] = {"$eq": plan_type}
    if state:
        filter_clauses["state"] = {"$eq": state}
    if clinical_area:
        filter_clauses["clinical_area"] = {"$eq": clinical_area}
    if adjudication_outcome:
        filter_clauses["adjudication_outcome"] = {"$eq": adjudication_outcome}

    if filter_clauses:
        vector_search_stage["filter"] = filter_clauses

    pipeline = [
        {"$vectorSearch": vector_search_stage},
        {
            "$project": {
                "_id": 0,
                "claim_id": 1,
                "member_id": 1,
                "plan_type": 1,
                "state": 1,
                "service_date": 1,
                "clinical_area": 1,
                "primary_diagnosis_code": 1,
                "primary_diagnosis_description": 1,
                "procedure_codes": 1,
                "billed_amount": 1,
                "adjudication_outcome": 1,
                "outcome_rationale": 1,
                "clinical_note": 1,
                "vector_score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    results = list(collection.aggregate(pipeline))
    return results, _displayable_pipeline(pipeline)
