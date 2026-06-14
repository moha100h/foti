from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from football_bot.services import data_provider as dp
from football_bot.services.engine import predict_fixtures
from football_bot.utils.formatting import fmt_fixture, fmt_prediction
from football_bot.keyboards.worldcup_menu import worldcup_menu_keyboard

router = Router()
LOADING = "\u062f\u0631 \u062d\u0627\u0644 \u062f\u0631\u06cc\u0627\u0641\u062a..."
WELCOME = "\U0001f3c6 <b>\u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc \u06f2\u06f0\u06f2\u06f6</b>\n\n\u0627\u0646\u062a\u062e\u0627\u0628 \u06a9\u0646\u06cc\u062f:"
T_FIX = "\U0001f3c6 <b>\u0628\u0627\u0632\u06cc\u200c\u0647\u0627\u06cc \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc</b>\n\n"
T_PRED = "\U0001f3af <b>\u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc</b>\n\n"
T_NONE = "\u062f\u0627\u062f\u0647\u200c\u0627\u06cc \u062f\u0631 \u062f\u0633\u062a\u0631\u0633 \u0646\u06cc\u0633\u062a."

@router.message(Command("worldcup"))
@router.message(F.text == "\U0001f3c6 \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc \u06f2\u06f0\u06f2\u06f6")
async def cmd_wc(message: Message):
    await message.answer(WELCOME, reply_markup=worldcup_menu_keyboard())

@router.callback_query(F.data == "wc_fixtures")
async def wc_fix(call: CallbackQuery):
    await call.answer()
    msg = await call.message.edit_text(LOADING)
    m = await dp.fixtures(0)
    wc = [x for x in m if "World Cup" in (x.get("league") or "")]
    data = wc or m
    if not data:
        await msg.edit_text(T_NONE, reply_markup=worldcup_menu_keyboard()); return
    await msg.edit_text(T_FIX + "".join(fmt_fixture(x) for x in data[:15]), reply_markup=worldcup_menu_keyboard())

@router.callback_query(F.data == "wc_preds")
async def wc_preds(call: CallbackQuery):
    await call.answer()
    msg = await call.message.edit_text(LOADING)
    up = await dp.upcoming_matches(10)
    fin = await dp.finished_matches(90)
    wc = [x for x in up if "World Cup" in (x.get("league") or "")]
    data = wc or up
    if not data:
        await msg.edit_text(T_NONE, reply_markup=worldcup_menu_keyboard()); return
    preds = predict_fixtures(data, fin)
    await msg.edit_text(T_PRED + "".join(fmt_prediction(p) + "\n" for p in preds[:6]), reply_markup=worldcup_menu_keyboard())
