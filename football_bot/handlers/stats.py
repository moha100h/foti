from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.stats_service import get_top_scorers, get_league_table
from football_bot.keyboards.stats_menu import stats_menu_keyboard

router = Router()

T_SELECT = "\u0628\u062e\u0634 \u0622\u0645\u0627\u0631 \u0631\u0627 \u0627\u0646\u062a\u062e\u0627\u0628 \u06a9\u0646\u06cc\u062f:"
T_LOADING = "\u062f\u0631 \u062d\u0627\u0644 \u062f\u0631\u06cc\u0627\u0641\u062a..."
T_NO_SCORERS = "\u0622\u0645\u0627\u0631 \u06af\u0644\u0632\u0646\u0627\u0646 \u062f\u0631 \u062f\u0633\u062a\u0631\u0633 \u0646\u06cc\u0633\u062a."
T_NO_TABLE = "\u062c\u062f\u0648\u0644 \u0644\u06cc\u06af \u062f\u0631 \u062f\u0633\u062a\u0631\u0633 \u0646\u06cc\u0633\u062a."
T_SOON = "\u0628\u0647 \u0632\u0648\u062f\u06cc \u0627\u0636\u0627\u0641\u0647 \u0645\u06cc\u200c\u0634\u0648\u062f."
T_SCORERS_H = "<b>\u0628\u0631\u062a\u0631\u06cc\u0646 \u06af\u0644\u0632\u0646\u0627\u0646 \u067e\u0631\u0645\u06cc\u0631 \u0644\u06cc\u06af</b>\n\n"
T_TABLE_H = "<b>\u062c\u062f\u0648\u0644 \u067e\u0631\u0645\u06cc\u0631 \u0644\u06cc\u06af</b>\n\n"
T_GOAL = " \u06af\u0644"
T_PTS = " \u0627\u0645\u062a\u06cc\u0627\u0632 ("
T_GAMES = " \u0628\u0627\u0632\u06cc)"


@router.message(Command("stats"))
@router.message(F.text == "\u0622\u0645\u0627\u0631")
async def cmd_stats(message: Message, db: AsyncSession):
    await message.answer(T_SELECT, reply_markup=stats_menu_keyboard())


@router.callback_query(F.data == "stats_scorers")
async def stats_scorers(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    msg = await call.message.edit_text(T_LOADING)
    scorers = await get_top_scorers(db)
    if not scorers:
        await msg.edit_text(T_NO_SCORERS, reply_markup=stats_menu_keyboard())
        return
    lines = [T_SCORERS_H]
    for i, s in enumerate(scorers[:10], 1):
        lines.append(str(i) + ". <b>" + s["name"] + "</b> (" + s["team"] + ") - " + str(s["goals"]) + T_GOAL + "\n")
    await msg.edit_text("".join(lines), reply_markup=stats_menu_keyboard())


@router.callback_query(F.data == "stats_table")
async def stats_table(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    msg = await call.message.edit_text(T_LOADING)
    table = await get_league_table(db)
    if not table:
        await msg.edit_text(T_NO_TABLE, reply_markup=stats_menu_keyboard())
        return
    lines = [T_TABLE_H]
    for t in table[:10]:
        lines.append(
            str(t["position"]) + ". <b>" + t["team"] + "</b>" +
            T_PTS + str(t["points"]) + T_GAMES + str(t["played"]) + ")\n"
        )
    await msg.edit_text("".join(lines), reply_markup=stats_menu_keyboard())


@router.callback_query(F.data == "stats_assists")
async def stats_assists(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    await call.message.edit_text(T_SOON, reply_markup=stats_menu_keyboard())
