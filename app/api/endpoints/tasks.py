import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas import TaskCreate, TaskOut
from app.services.task_service import create_task, list_tasks

router = APIRouter(prefix="/tasks")


@router.post("", response_model=TaskOut)
def import_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, external_id=task_in.external_id, input_text=task_in.input_text)


@router.post("/mock", response_model=TaskOut)
def create_mock_task(db: Session = Depends(get_db)):
    return create_task(
        db,
        external_id=f"mock_{uuid.uuid4().hex[:8]}",
        input_text="Отличный сервис, очень доволен!",
    )


@router.get("", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return list_tasks(db)
