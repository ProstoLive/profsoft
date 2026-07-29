import time

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.api.endpoints import health, tasks
from app.db.database import Base, engine
from app.models import database_models  # noqa: F401

app = FastAPI(title="AI microservice skeleton")


def create_tables_with_retry(attempts: int = 10, delay_seconds: float = 1.5) -> None:
    for attempt in range(1, attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == attempts:
                raise
            time.sleep(delay_seconds)


create_tables_with_retry()

app.include_router(health.router)
app.include_router(tasks.router)
