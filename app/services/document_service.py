from sqlalchemy.orm import Session

from app.models.database_models import Document


def create_document(db: Session, source: str, text: str) -> Document:
    document = Document(source=source, text=text, status="idle")
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def list_idle_documents(db: Session) -> list[Document]:
    return db.query(Document).filter(Document.status == "idle").all()
