from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from football_bot.services import data_provider as dp
from football_bot.services.engine import predict_fixtures
from football_bot.utils.formatting import fmt_prediction
from football_bot.keyboards.predictions_menu import predictions_menu_keyboard

router = Router()
LOADING = "\U0001f9e0 \u062f\u0631 \u062d\u0627\u0644 \u062a\u062d\u0644\u06cc\u0644..."
T_NONE = "\u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc \u062f\u0631 \u062f\u0633\u062a\u0631\u0633 \u0646\u06cc\u0633\u062a."
T_TOP = "\U0001f3af <b>\u0628\u0647\u062a\u0631\u06cc\u0646 \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc\u200c\u0647\u0627</b>\n<i>Poisson + Elo</i>\n\n"
T_OU = "\u26bd <b>\u0628\u0627\u0644\u0627\u06cc \u06f2.\u06f5 \u06af\u0644</b>\n\n"
T_BTTS = "\U0001f3af <b>\u0647\u0631\u062f\u0648 \u062a\u06cc\u0645 \u06af\u0644</b>\n\n"

async def _preds():
    up = await dp.upcoming_matches(7)
    fin = await dp.finished_matches(60)
    if not up: return []
    return predict_fixtures(up, fin)

@router.message(Command("predictions"))
@router.message(F.text == "\U0001f3af \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc\u200c\u0647\u0627")
async def cmd_pred(message: Message):
    await message.answer("\u0646\u0648\u0639 \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc:", reply_markup=predictions_menu_keyboard())

async def _send(call, title, sort_key):
    msg = await call.message.edit_text(LOADING)
    preds = await _preds()
    if not preds:
        await msg.edit_text(T_NONE, reply_markup=predictions_menu_keyboard()); return
    if sort_key:
        preds.sort(key=lambda x: x[sort_key], reverse=True)
    await msg.edit_text(title + "".join(fmt_prediction(p) + "\n" for p in preds[:6]), reply_markup=predictions_menu_keyboard())

@router.callback_query(F.data == "pred_top")
async def pred_top(call: CallbackQuery):
    await call.answer(); await _send(call, T_TOP, None)

@router.callback_query(F.data == "pred_ou")
async def pred_ou(call: CallbackQuery):
    await call.answer(); await _send(call, T_OU, "p_over25")

@router.callback_query(F.data == "pred_btts")
async def pred_btts(call: CallbackQuery):
    await call.answer(); await _send(call, T_BTTS, "p_btts")
