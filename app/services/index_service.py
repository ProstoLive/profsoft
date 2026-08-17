import logging
import uuid

from qdrant_client.models import PointStruct
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database_models import Document
from app.services.chunking import split_text
from app.services.embeddings import embed_texts
from app.vector.qdrant_client import client as qdrant_client

logger = logging.getLogger(__name__)


def index_document(db: Session, document: Document) -> None:
    document.status = "syncing"
    db.commit()

    try:
        chunks = split_text(document.text, settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
        vectors = embed_texts(chunks)

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk,
                    "source": document.source,
                    "doc_id": document.id,
                    "section": i,
                },
            )
            for i, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]
        qdrant_client.upsert(collection_name=settings.COLLECTION, points=points)

        document.status = "indexed"
        db.commit()
        logger.info("document %s: syncing -> indexed (%s chunks)", document.id, len(points))
    except Exception as e:
        document.status = "failed"
        db.commit()
        logger.warning("document %s: indexing failed (%s)", document.id, e)
