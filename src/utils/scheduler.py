import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from functools import partial

from src.config import settings

logger = logging.getLogger(__name__)


async def safe_sync(sync_service):
    try:
        await sync_service.sync_all()
    except Exception as e:
        logger.exception(f"Scheduled sync failed: {e}")


def start_scheduler(sync_service):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        partial(safe_sync, sync_service),
        trigger=IntervalTrigger(hours=settings.SYNC_INTERVAL_HOURS),
        id="daily_sync",
        name="Daily sync from jsonplaceholder",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Scheduler started with daily sync job")
