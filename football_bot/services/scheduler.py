from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from aiogram import Bot
import pytz

# Use pytz timezone — safe on all Linux distros without tzdata package
TEHRAN_TZ = pytz.timezone("Asia/Tehran")

scheduler = AsyncIOScheduler(timezone=TEHRAN_TZ)
_bot: Bot = None


async def _heartbeat():
    """Periodic heartbeat — logs scheduler is alive."""
    logger.debug("Scheduler heartbeat")


async def start_scheduler(bot: Bot):
    global _bot
    _bot = bot
    # Heartbeat every 5 minutes
    scheduler.add_job(_heartbeat, IntervalTrigger(minutes=5), id="heartbeat", replace_existing=True)
    scheduler.start()
    logger.info("Scheduler started (Asia/Tehran)")


async def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")
