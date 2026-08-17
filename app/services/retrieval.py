from app.core.config import settings
from app.services.embeddings import embed_texts
from app.vector.qdrant_client import client as qdrant_client


def search(question: str, k: int) -> list:
    query_vector = embed_texts([question])[0]
    result = qdrant_client.query_points(
        collection_name=settings.COLLECTION,
        query=query_vector,
        limit=k,
        with_payload=True,
    )
    return result.points
