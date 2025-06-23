import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from functools import partial
from src.exceptions import AppException
from src.services.sync_service import SyncService

logger = logging.getLogger(__name__)


async def safe_sync(sync_service: SyncService) -> None:
    try:
        await sync_service.sync_all()
        logger.info("Scheduled sync completed successfully")
    except Exception as e:
        logger.exception("Scheduled sync failed", e)
        raise AppException("Scheduled sync failed") from e


def start_scheduler(sync_service: SyncService) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    try:
        scheduler.add_job(
            partial(safe_sync, sync_service),
            trigger=IntervalTrigger(hours=24),
            id="daily_sync",
            name="Daily sync from jsonplaceholder",
            replace_existing=True,
        )

        scheduler.start()
        logger.info("Scheduler started with daily sync job")

    except Exception as e:
        logger.exception("Failed to start scheduler", e)
        raise AppException

    return scheduler
