from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.stats_service import get_top_scorers
from football_bot.keyboards.stats_menu import stats_menu_keyboard

router = Router()


@router.message(Command("stats"))
@router.message(F.text == "آمار")
async def cmd_stats(message: Message, db: AsyncSession):
    await message.answer("بخش آمار را انتخاب کنید:", reply_markup=stats_menu_keyboard())


@router.callback_query(F.data == "stats_scorers")
async def stats_scorers(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    scorers = await get_top_scorers(db)
    if not scorers:
        await call.message.edit_text("آمار گلزنان در دسترس نیست.", reply_markup=stats_menu_keyboard())
        return
    text = "<b>برترین گلزنان</b>

"
    for i, s in enumerate(scorers[:10], 1):
        text += f"{i}. {s['name']} ({s['team']}) - {s['goals']} گل
"
    await call.message.edit_text(text, reply_markup=stats_menu_keyboard())
