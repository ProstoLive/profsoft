import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.db.database import SessionLocal
from app.services.ai_service import classify
from app.services.export_service import send_result
from app.services.task_service import (
    claim_one_pending,
    list_done_for_export,
    mark_done,
    mark_failed_or_retry,
    mark_sent,
    reset_stuck,
)

logger = logging.getLogger(__name__)


def process_pending() -> None:
    db = SessionLocal()
    try:
        task = claim_one_pending(db)
        if task is None:
            return

        try:
            result = classify(task.input_text)
            mark_done(db, task, result)
            logger.info("task %s: processing -> done", task.external_id)
        except Exception as e:
            mark_failed_or_retry(db, task, str(e))
            logger.warning("task %s: processing failed (%s), attempts=%s", task.external_id, e, task.attempts)
    finally:
        db.close()


def export_done() -> None:
    db = SessionLocal()
    try:
        for task in list_done_for_export(db):
            try:
                if send_result(task):
                    mark_sent(db, task)
                    logger.info("task %s: done -> sent", task.external_id)
            except Exception as e:
                logger.warning("task %s: export failed (%s)", task.external_id, e)
    finally:
        db.close()


def reset_stuck_job() -> None:
    db = SessionLocal()
    try:
        n = reset_stuck(db)
        if n > 0:
            logger.info("reset %s stuck task(s) processing -> pending", n)
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_pending, "interval", seconds=settings.POLL_INTERVAL)
    scheduler.add_job(export_done, "interval", seconds=settings.POLL_INTERVAL)
    scheduler.add_job(reset_stuck_job, "interval", seconds=60)
    scheduler.start()
    logger.info("scheduler started: poll_interval=%ss", settings.POLL_INTERVAL)
    return scheduler
