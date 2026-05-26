"""
Hybrid search via $rankFusion — combines $vectorSearch (semantic) and
$search (lexical) sub-pipelines over the same collection, applying
identical hard filters to both so the comparison is apples-to-apples.

Per-pipeline ranks are surfaced on each result via scoreDetails so the
UI can show how each result was contributed by the vector vs. lexical
sub-pipeline.
"""

from copy import deepcopy
from typing import List, Optional, Tuple
from pymongo.collection import Collection


POLICIES_VECTOR_INDEX = "policy_vector_index"
POLICIES_SEARCH_INDEX = "policy_search_index"
PRIOR_CLAIMS_VECTOR_INDEX = "prior_claims_vector_index"
PRIOR_CLAIMS_SEARCH_INDEX = "prior_claims_search_index"

# How many candidates each sub-pipeline contributes before fusion.
# Larger = more chance for one pipeline to surface a result the other
# missed, at the cost of more work per query.
NUM_CANDIDATES = 80
SUBPIPELINE_LIMIT = 20

# Truncate the lexical query to a sane length; clinical_notes can be
# multi-paragraph and most signal is in the first chunk.
MAX_LEXICAL_QUERY_CHARS = 1000


def _displayable_pipeline(pipeline: List[dict]) -> List[dict]:
    """Replace the 1024-dim queryVector inside the $rankFusion stage with a
    short placeholder so the JSON stays readable when shown in the UI."""
    redacted = deepcopy(pipeline)
    for stage in redacted:
        rf = stage.get("$rankFusion")
        if not rf:
            continue
        for _name, sub_pipe in rf.get("input", {}).get("pipelines", {}).items():
            for sub_stage in sub_pipe:
                vs = sub_stage.get("$vectorSearch")
                if vs and "queryVector" in vs:
                    dims = len(vs["queryVector"]) if isinstance(vs["queryVector"], list) else "?"
                    vs["queryVector"] = f"<{dims}-dim embedding from step 2>"
    return redacted


def _extract_ranks(score_details):
    """Pull (vector_rank, lexical_rank) out of $rankFusion scoreDetails.
    A pipeline that did not surface this document returns None for its rank."""
    vector_rank: Optional[int] = None
    lexical_rank: Optional[int] = None
    if not score_details:
        return vector_rank, lexical_rank
    for detail in score_details.get("details", []):
        name = detail.get("inputPipelineName")
        rank = detail.get("rank")
        if name == "vector":
            vector_rank = rank
        elif name == "lexical":
            lexical_rank = rank
    return vector_rank, lexical_rank


def _trim_query(text: str) -> str:
    if not text:
        return ""
    return text[:MAX_LEXICAL_QUERY_CHARS]


def hybrid_search_policies(
    collection: Collection,
    query_vector: List[float],
    query_text: str,
    limit: int = 3,
    clinical_area: Optional[str] = None,
) -> Tuple[List[dict], List[dict]]:
    """
    Hybrid search the policies collection — vector + lexical fused via
    $rankFusion. The clinical_area filter is applied to both sub-pipelines.

    Returns (results, displayable_pipeline). Each result includes
    `vector_rank` and `lexical_rank` (int or None).
    """
    vs_stage: dict = {
        "$vectorSearch": {
            "index": POLICIES_VECTOR_INDEX,
            "path": "clinical_embedding",
            "queryVector": query_vector,
            "numCandidates": NUM_CANDIDATES,
            "limit": SUBPIPELINE_LIMIT,
        }
    }
    if clinical_area:
        vs_stage["$vectorSearch"]["filter"] = {"clinical_area": {"$eq": clinical_area}}

    search_compound: dict = {
        "must": [
            {
                "text": {
                    "query": _trim_query(query_text),
                    "path": ["title", "criteria_text", "subcategory"],
                }
            }
        ],
    }
    if clinical_area:
        search_compound["filter"] = [
            {"equals": {"path": "clinical_area", "value": clinical_area}}
        ]

    search_stage = {
        "$search": {
            "index": POLICIES_SEARCH_INDEX,
            "compound": search_compound,
        }
    }

    pipeline = [
        {
            "$rankFusion": {
                "input": {
                    "pipelines": {
                        "vector": [vs_stage],
                        "lexical": [search_stage, {"$limit": SUBPIPELINE_LIMIT}],
                    }
                },
                "combination": {"weights": {"vector": 1, "lexical": 1}},
                "scoreDetails": True,
            }
        },
        {"$limit": limit},
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
                "_score_details": {"$meta": "scoreDetails"},
            }
        },
    ]

    raw = list(collection.aggregate(pipeline))
    results = []
    for r in raw:
        details = r.pop("_score_details", None)
        v_rank, l_rank = _extract_ranks(details)
        r["vector_rank"] = v_rank
        r["lexical_rank"] = l_rank
        results.append(r)

    return results, _displayable_pipeline(pipeline)


def hybrid_search_prior_claims(
    collection: Collection,
    query_vector: List[float],
    query_text: str,
    limit: int = 3,
    plan_type: Optional[str] = None,
    state: Optional[str] = None,
    clinical_area: Optional[str] = None,
    adjudication_outcome: Optional[str] = None,
) -> Tuple[List[dict], List[dict]]:
    """
    Hybrid search prior_claims — vector + lexical fused via $rankFusion.
    All hard filters are mirrored across both sub-pipelines so each one
    sees the same constrained candidate set.
    """
    vs_filter: dict = {}
    if plan_type:
        vs_filter["plan_type"] = {"$eq": plan_type}
    if state:
        vs_filter["state"] = {"$eq": state}
    if clinical_area:
        vs_filter["clinical_area"] = {"$eq": clinical_area}
    if adjudication_outcome:
        vs_filter["adjudication_outcome"] = {"$eq": adjudication_outcome}

    vs_stage: dict = {
        "$vectorSearch": {
            "index": PRIOR_CLAIMS_VECTOR_INDEX,
            "path": "clinical_embedding",
            "queryVector": query_vector,
            "numCandidates": NUM_CANDIDATES,
            "limit": SUBPIPELINE_LIMIT,
        }
    }
    if vs_filter:
        vs_stage["$vectorSearch"]["filter"] = vs_filter

    search_filter: list = []
    if plan_type:
        search_filter.append({"equals": {"path": "plan_type", "value": plan_type}})
    if state:
        search_filter.append({"equals": {"path": "state", "value": state}})
    if clinical_area:
        search_filter.append({"equals": {"path": "clinical_area", "value": clinical_area}})
    if adjudication_outcome:
        search_filter.append(
            {"equals": {"path": "adjudication_outcome", "value": adjudication_outcome}}
        )

    search_compound: dict = {
        "must": [
            {
                "text": {
                    "query": _trim_query(query_text),
                    "path": [
                        "clinical_note",
                        "outcome_rationale",
                        "primary_diagnosis_description",
                    ],
                }
            }
        ],
    }
    if search_filter:
        search_compound["filter"] = search_filter

    search_stage = {
        "$search": {
            "index": PRIOR_CLAIMS_SEARCH_INDEX,
            "compound": search_compound,
        }
    }

    pipeline = [
        {
            "$rankFusion": {
                "input": {
                    "pipelines": {
                        "vector": [vs_stage],
                        "lexical": [search_stage, {"$limit": SUBPIPELINE_LIMIT}],
                    }
                },
                "combination": {"weights": {"vector": 1, "lexical": 1}},
                "scoreDetails": True,
            }
        },
        {"$limit": limit},
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
                "_score_details": {"$meta": "scoreDetails"},
            }
        },
    ]

    raw = list(collection.aggregate(pipeline))
    results = []
    for r in raw:
        details = r.pop("_score_details", None)
        v_rank, l_rank = _extract_ranks(details)
        r["vector_rank"] = v_rank
        r["lexical_rank"] = l_rank
        results.append(r)

    return results, _displayable_pipeline(pipeline)
