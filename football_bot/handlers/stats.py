from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from football_bot.services import data_provider as dp
from football_bot.utils.formatting import fmt_scorer, fmt_table_row
from football_bot.keyboards.stats_menu import stats_menu_keyboard

router = Router()
LOADING = "\u062f\u0631 \u062d\u0627\u0644 \u062f\u0631\u06cc\u0627\u0641\u062a..."
T_SCORERS = "\u26bd <b>\u0628\u0631\u062a\u0631\u06cc\u0646 \u06af\u0644\u0632\u0646\u0627\u0646 \u067e\u0631\u0645\u06cc\u0631\u0644\u06cc\u06af</b>\n\n"
T_TABLE = "\U0001f4cb <b>\u062c\u062f\u0648\u0644 \u067e\u0631\u0645\u06cc\u0631\u0644\u06cc\u06af</b>\n\n"
T_NONE = "\u0622\u0645\u0627\u0631 \u062f\u0631 \u062f\u0633\u062a\u0631\u0633 \u0646\u06cc\u0633\u062a."

@router.message(Command("stats"))
@router.message(F.text == "\U0001f4ca \u0622\u0645\u0627\u0631")
async def cmd_stats(message: Message):
    await message.answer("\u0628\u062e\u0634 \u0622\u0645\u0627\u0631:", reply_markup=stats_menu_keyboard())

@router.callback_query(F.data == "stats_scorers")
async def scorers(call: CallbackQuery):
    await call.answer()
    msg = await call.message.edit_text(LOADING)
    data = await dp.top_scorers("PL")
    if not data:
        await msg.edit_text(T_NONE, reply_markup=stats_menu_keyboard()); return
    body = "".join(fmt_scorer(i, s) for i, s in enumerate(data[:10], 1))
    await msg.edit_text(T_SCORERS + body, reply_markup=stats_menu_keyboard())

@router.callback_query(F.data == "stats_table")
async def table(call: CallbackQuery):
    await call.answer()
    msg = await call.message.edit_text(LOADING)
    data = await dp.standings("PL")
    if not data:
        await msg.edit_text(T_NONE, reply_markup=stats_menu_keyboard()); return
    body = "".join(fmt_table_row(t) for t in data[:12])
    await msg.edit_text(T_TABLE + body, reply_markup=stats_menu_keyboard())
