import httpx
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database_models import Task
from app.services.task_service import create_task


class SourceComment(BaseModel):
    id: int
    body: str


def import_tasks_from_source(db: Session) -> list[Task]:
    response = httpx.get(settings.API_URL, timeout=10)
    response.raise_for_status()

    comments = [SourceComment.model_validate(item) for item in response.json()]
    return [
        create_task(db, external_id=f"api_{comment.id}", input_text=comment.body)
        for comment in comments
    ]
