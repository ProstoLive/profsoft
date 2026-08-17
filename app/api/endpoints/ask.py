from fastapi import APIRouter

from app.models.schemas import AskRequest, AskResponse
from app.services.rag_service import answer

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return answer(request.question)
