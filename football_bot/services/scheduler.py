from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from aiogram import Bot

scheduler = AsyncIOScheduler(timezone="Asia/Tehran")

async def start_scheduler(bot: Bot):
    scheduler.start()
    logger.info("Scheduler started")

async def stop_scheduler():
    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")
