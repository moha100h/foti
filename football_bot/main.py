import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from football_bot.config import settings
from football_bot.database import init_db, close_db
from football_bot.handlers import router
from football_bot.middleware import setup_middlewares
from football_bot.services.scheduler import start_scheduler, stop_scheduler


async def main():
    logger.add(
        settings.LOG_FILE, rotation="10 MB", retention="7 days", level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    )
    logger.info("Starting Foti Football Bot...")
    await init_db()
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    setup_middlewares(dp)
    dp.include_router(router)
    await start_scheduler(bot)
    try:
        logger.info("Bot polling started")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await stop_scheduler()
        await close_db()
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
