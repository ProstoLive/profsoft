import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.api.endpoints import ask, documents, health, tasks
from app.core.config import settings
from app.db.database import Base, engine
from app.models import database_models  # noqa: F401
from app.vector.qdrant_client import ensure_collection
from app.workers.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def create_tables_with_retry(attempts: int = 10, delay_seconds: float = 1.5) -> None:
    for attempt in range(1, attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == attempts:
                raise
            time.sleep(delay_seconds)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables_with_retry()
    ensure_collection()

    scheduler = start_scheduler() if settings.RUN_WORKER else None
    yield
    if scheduler is not None:
        scheduler.shutdown()


app = FastAPI(title="AI microservice skeleton", lifespan=lifespan)

app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(documents.router)
app.include_router(ask.router)
