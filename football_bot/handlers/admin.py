from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from football_bot.config import settings
from football_bot.keyboards.admin_menu import admin_menu_keyboard
from football_bot.models.user import User

router = Router()
NO_ACCESS = "\u062f\u0633\u062a\u0631\u0633\u06cc \u0646\u062f\u0627\u0631\u06cc\u062f."

def is_admin(uid):
    return uid in settings.ADMIN_IDS

@router.message(Command("admin"))
async def cmd_admin(message: Message, db: AsyncSession):
    if not is_admin(message.from_user.id):
        await message.answer(NO_ACCESS); return
    users = await db.scalar(select(func.count(User.telegram_id)))
    text = ("\U0001f6e0\ufe0f <b>\u067e\u0646\u0644 \u0645\u062f\u06cc\u0631\u06cc\u062a</b>\n\n"
            "\U0001f465 \u06a9\u0627\u0631\u0628\u0631\u0627\u0646: " + str(users or 0))
    await message.answer(text, reply_markup=admin_menu_keyboard())

@router.callback_query(F.data == "admin_refresh")
async def refresh(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer(NO_ACCESS, show_alert=True); return
    from football_bot.services import data_provider as dp
    dp._cache.clear()
    await call.answer("\u06a9\u0634 \u067e\u0627\u06a9 \u0634\u062f \u2714\ufe0f", show_alert=True)

@router.callback_query(F.data == "admin_broadcast")
async def broadcast(call: CallbackQuery):
    if not is_admin(call.from_user.id):
        await call.answer(NO_ACCESS, show_alert=True); return
    await call.message.edit_text("\u067e\u06cc\u0627\u0645 \u0647\u0645\u06af\u0627\u0646\u06cc \u0631\u0627 \u0628\u0646\u0648\u06cc\u0633\u06cc\u062f.")
