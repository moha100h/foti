from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.config import settings
from football_bot.keyboards.admin_menu import admin_menu_keyboard
from football_bot.services.stats_service import get_bot_stats

router = Router()

MSG_NO_ACCESS = "دسترسی ندارید."


def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message, db: AsyncSession):
    if not is_admin(message.from_user.id):
        await message.answer(MSG_NO_ACCESS)
        return
    stats = await get_bot_stats(db)
    lines = [
        "<b>پنل مدیریت</b>",
        "",
        "کاربران: " + str(stats.get("users", 0)),
        "پیش‌بینی‌ها: " + str(stats.get("predictions", 0)),
        "بازی‌های ذخیره‌شده: " + str(stats.get("matches", 0)),
    ]
    await message.answer("\n".join(lines), reply_markup=admin_menu_keyboard())


@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(call: CallbackQuery, db: AsyncSession):
    if not is_admin(call.from_user.id):
        await call.answer(MSG_NO_ACCESS, show_alert=True)
        return
    await call.message.edit_text("پیام خود را برای ارسال به همه کاربران بنویسید:")
