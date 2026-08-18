from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.core.config import settings
from app.services.embeddings import embed_texts
from app.vector.qdrant_client import client as qdrant_client


def search(question: str, k: int, doc_id: int | None = None) -> list:
    query_vector = embed_texts([question])[0]

    query_filter = None
    if doc_id is not None:
        query_filter = Filter(must=[FieldCondition(key="doc_id", match=MatchValue(value=doc_id))])

    result = qdrant_client.query_points(
        collection_name=settings.COLLECTION,
        query=query_vector,
        query_filter=query_filter,
        limit=k,
        score_threshold=settings.SCORE_THRESHOLD,
        with_payload=True,
    )
    return result.points
