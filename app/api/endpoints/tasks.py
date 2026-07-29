from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.schemas import TaskOut
from app.services.task_service import create_task, list_tasks

router = APIRouter(prefix="/tasks")


@router.post("/mock", response_model=TaskOut)
def create_mock_task(db: Session = Depends(get_db)):
    return create_task(db, external_id="test_001")


@router.get("", response_model=list[TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    return list_tasks(db)
