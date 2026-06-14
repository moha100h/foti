from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services import data_provider as dp, settings_service as ss
from football_bot.services.engine import predict_fixtures
from football_bot.utils.formatting import fmt_fixture, fmt_prediction
from football_bot.keyboards.worldcup_menu import worldcup_menu_keyboard, wc_live_refresh_keyboard

router = Router()
LOADING = "\u062f\u0631 \u062d\u0627\u0644 \u062f\u0631\u06cc\u0627\u0641\u062a..."
WELCOME = "\U0001f3c6 <b>\u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc \u06f2\u06f0\u06f2\u06f6</b>\n\n\u0627\u0646\u062a\u062e\u0627\u0628 \u06a9\u0646:"
T_FIX = "\U0001f3c6 <b>\u0628\u0627\u0632\u06cc\u200c\u0647\u0627\u06cc \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc</b>\n\n"
T_PRED = "\U0001f3af <b>\u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc</b>\n\n"
T_LIVE = "\U0001f534 <b>\u0628\u0627\u0632\u06cc\u200c\u0647\u0627\u06cc \u0632\u0646\u062f\u0647 \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc</b>\n\n"
T_NONE = "\u062f\u0627\u062f\u0647\u200c\u0627\u06cc \u062f\u0631 \u062f\u0633\u062a\u0631\u0633 \u0646\u06cc\u0633\u062a."
T_NOLIVE = "\u062f\u0631 \u062d\u0627\u0644 \u062d\u0627\u0636\u0631 \u0628\u0627\u0632\u06cc \u0632\u0646\u062f\u0647\u200c\u0627\u06cc \u0646\u06cc\u0633\u062a."

def _is_wc(x):
    return "World Cup" in (x.get("league") or "")

def _fmt_live(m):
    minute = m.get("minute") or ""
    mtxt = f" \u23f1{minute}'" if minute else " \U0001f534"
    return (f"\u26bd <b>{m.get('home','')}</b> {m.get('home_score',0)} - "
            f"{m.get('away_score',0)} <b>{m.get('away','')}</b>{mtxt}\n")

@router.message(Command("worldcup"))
@router.message(F.text == "\U0001f3c6 \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc \u06f2\u06f0\u06f2\u06f6")
async def cmd_wc(message: Message):
    await message.answer(WELCOME, reply_markup=worldcup_menu_keyboard())

@router.callback_query(F.data == "wc_back")
async def wc_back(call: CallbackQuery):
    await call.answer()
    try:
        await call.message.edit_text(WELCOME, reply_markup=worldcup_menu_keyboard())
    except Exception:
        await call.message.answer(WELCOME, reply_markup=worldcup_menu_keyboard())

@router.callback_query(F.data == "wc_live")
async def wc_live(call: CallbackQuery):
    await call.answer("\u0628\u0647\u200c\u0631\u0648\u0632\u0631\u0633\u0627\u0646\u06cc...")
    try:
        msg = await call.message.edit_text(LOADING)
    except Exception:
        msg = await call.message.answer(LOADING)
    live = await dp.live_matches()
    wc = [x for x in live if _is_wc(x)]
    data = wc or live
    if not data:
        await msg.edit_text(T_NOLIVE, reply_markup=wc_live_refresh_keyboard()); return
    await msg.edit_text(T_LIVE + "".join(_fmt_live(x) for x in data[:15]), reply_markup=wc_live_refresh_keyboard())

@router.callback_query(F.data == "wc_fixtures")
async def wc_fix(call: CallbackQuery):
    await call.answer()
    msg = await call.message.edit_text(LOADING)
    m = await dp.fixtures(0)
    wc = [x for x in m if _is_wc(x)]
    data = wc or m
    if not data:
        await msg.edit_text(T_NONE, reply_markup=worldcup_menu_keyboard()); return
    await msg.edit_text(T_FIX + "".join(fmt_fixture(x) for x in data[:15]), reply_markup=worldcup_menu_keyboard())

@router.callback_query(F.data == "wc_preds")
async def wc_preds(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    msg = await call.message.edit_text(LOADING)
    up = await dp.upcoming_matches(10); fin = await dp.finished_matches(90)
    wc = [x for x in up if _is_wc(x)]
    data = wc or up
    if not data:
        await msg.edit_text(T_NONE, reply_markup=worldcup_menu_keyboard()); return
    preds = predict_fixtures(data, fin, home_adv=ss.cfloat("HOME_ADV"), league_avg=ss.cfloat("LEAGUE_AVG"),
                             rho=ss.cfloat("DC_RHO"), elo_weight=ss.cfloat("ELO_WEIGHT"), half_life=ss.cfloat("HALF_LIFE_DAYS"))
    await msg.edit_text(T_PRED + "".join(fmt_prediction(p) + "\n" for p in preds[:6]), reply_markup=worldcup_menu_keyboard())
