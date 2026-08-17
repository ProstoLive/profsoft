from app.ai.client import client
from app.core.config import settings


def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=settings.EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]
