"""
Voyage AI embedding service.

Generates 1024-dimension embeddings using voyage-3. The embedding is stored
directly in the MongoDB document alongside the operational data — no separate
vector store, no synchronization required.
"""

from typing import Optional
import voyageai
from config import settings

_client: Optional[voyageai.Client] = None


def _get_client() -> voyageai.Client:
    global _client
    if _client is None:
        _client = voyageai.Client(api_key=settings.voyage_api_key)
    return _client


def embed_document(text: str) -> list[float]:
    """Embed a document-mode text (for indexing clinical notes)."""
    result = _get_client().embed(
        texts=[text],
        model="voyage-3",
        input_type="document",
    )
    return result.embeddings[0]


def embed_query(text: str) -> list[float]:
    """Embed a query-mode text (for similarity search)."""
    result = _get_client().embed(
        texts=[text],
        model="voyage-3",
        input_type="query",
    )
    return result.embeddings[0]


def embed_batch(texts: list[str], input_type: str = "document") -> list[list[float]]:
    """Embed multiple texts in one API call (more efficient for seeding)."""
    # Voyage AI max batch is 128 texts; split if larger
    BATCH_SIZE = 64
    all_embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        result = _get_client().embed(
            texts=batch,
            model="voyage-3",
            input_type=input_type,
        )
        all_embeddings.extend(result.embeddings)
    return all_embeddings
