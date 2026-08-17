import time

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings

client = QdrantClient(url=settings.QDRANT_URL)


def ensure_collection(attempts: int = 10, delay_seconds: float = 1.5) -> None:
    for attempt in range(1, attempts + 1):
        try:
            if not client.collection_exists(settings.COLLECTION):
                client.create_collection(
                    collection_name=settings.COLLECTION,
                    vectors_config=VectorParams(size=settings.EMBED_DIM, distance=Distance.COSINE),
                )
            return
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(delay_seconds)
