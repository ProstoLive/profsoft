from sqlalchemy.orm import Session

from app.models.database_models import Task


def create_task(db: Session, external_id: str) -> Task:
    existing = db.query(Task).filter(Task.external_id == external_id).first()
    if existing:
        return existing

    task = Task(external_id=external_id, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.created_at.desc()).all()
