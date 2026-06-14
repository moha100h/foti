from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.config import settings
from football_bot.keyboards.admin_menu import admin_menu_keyboard
from football_bot.services.stats_service import get_bot_stats

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message, db: AsyncSession):
    if not is_admin(message.from_user.id):
        await message.answer("دسترسی ندارید.")
        return
    stats = await get_bot_stats(db)
    text = (
        "<b>پنل مدیریت</b>

"
        f"کاربران: {stats.get('users', 0)}
"
        f"پیش‌بینی‌ها: {stats.get('predictions', 0)}
"
        f"بازی‌های ذخیره‌شده: {stats.get('matches', 0)}
"
    )
    await message.answer(text, reply_markup=admin_menu_keyboard())
