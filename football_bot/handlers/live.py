from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.live_service import get_live_matches
from football_bot.keyboards.live_menu import live_refresh_keyboard
from football_bot.utils.formatting import format_live_match

router = Router()

MSG_NO_LIVE = "در حال حاضر بازی زندهای وجود ندارد."
MSG_LOADING = "در حال دریافت نتایج زنده..."
MSG_REFRESHING = "در حال به‌روزرسانی..."
MSG_TITLE = "<b>نتایج زنده</b>\n\n"


@router.message(Command("live"))
@router.message(F.text == "نتایج زنده")
async def cmd_live(message: Message, db: AsyncSession):
    msg = await message.answer(MSG_LOADING)
    matches = await get_live_matches()
    if not matches:
        await msg.edit_text(MSG_NO_LIVE, reply_markup=live_refresh_keyboard())
        return
    text = MSG_TITLE + "".join(format_live_match(m) + "\n" for m in matches[:10])
    await msg.edit_text(text, reply_markup=live_refresh_keyboard())


@router.callback_query(F.data == "refresh_live")
async def refresh_live(call: CallbackQuery, db: AsyncSession):
    await call.answer(MSG_REFRESHING)
    matches = await get_live_matches()
    if not matches:
        await call.message.edit_text(MSG_NO_LIVE, reply_markup=live_refresh_keyboard())
        return
    text = MSG_TITLE + "".join(format_live_match(m) + "\n" for m in matches[:10])
    await call.message.edit_text(text, reply_markup=live_refresh_keyboard())
