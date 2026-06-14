from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.stats_service import get_top_scorers
from football_bot.keyboards.stats_menu import stats_menu_keyboard

router = Router()

MSG_SELECT = "بخش آمار را انتخاب کنید:"
MSG_NO_SCORERS = "آمار گلزنان در دسترس نیست."
MSG_SCORERS_TITLE = "<b>برترین گلزنان</b>\n\n"


@router.message(Command("stats"))
@router.message(F.text == "آمار")
async def cmd_stats(message: Message, db: AsyncSession):
    await message.answer(MSG_SELECT, reply_markup=stats_menu_keyboard())


@router.callback_query(F.data == "stats_scorers")
async def stats_scorers(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    scorers = await get_top_scorers(db)
    if not scorers:
        await call.message.edit_text(MSG_NO_SCORERS, reply_markup=stats_menu_keyboard())
        return
    lines = [MSG_SCORERS_TITLE]
    for i, s in enumerate(scorers[:10], 1):
        lines.append(str(i) + ". " + s["name"] + " (" + s["team"] + ") - " + str(s["goals"]) + " گل\n")
    await call.message.edit_text("".join(lines), reply_markup=stats_menu_keyboard())
