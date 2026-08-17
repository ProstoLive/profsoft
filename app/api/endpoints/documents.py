from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas import DocumentCreate, DocumentOut
from app.services.document_service import create_document

router = APIRouter(prefix="/documents")


@router.post("", response_model=DocumentOut)
def import_document(document_in: DocumentCreate, db: Session = Depends(get_db)):
    return create_document(db, source=document_in.source, text=document_in.text)
