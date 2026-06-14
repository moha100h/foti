from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.keyboards.predictions_menu import value_menu_keyboard
from football_bot.services import settings_service as ss, value as vv, bet_service as bs
from football_bot.services import data_provider as dp, engine

router = Router()

INTRO = ("\U0001f4b0 <b>\u0634\u0631\u0637\u200c\u0647\u0627\u06cc \u0627\u0631\u0632\u0634\u0645\u0646\u062f</b>\n\n"
         "\u0645\u062f\u0644 \u0631\u0627 \u0628\u0627 \u0636\u0631\u0627\u06cc\u0628 \u0628\u0648\u06a9\u0645\u06cc\u06a9\u0631 \u0645\u0642\u0627\u06cc\u0633\u0647 \u0645\u06cc\u200c\u06a9\u0646\u0645 \u0648 \u0641\u0642\u0637 \u0634\u0631\u0637\u200c\u0647\u0627\u06cc \u0628\u0627 Edge \u0645\u062b\u0628\u062a \u0631\u0627 \u0646\u0634\u0627\u0646 \u0645\u06cc\u200c\u062f\u0647\u0645.")

@router.message(Command("value"))
@router.message(F.text == "\U0001f4b0 \u0634\u0631\u0637\u200c\u0647\u0627\u06cc \u0627\u0631\u0632\u0634\u0645\u0646\u062f")
async def value_menu(message: Message):
    await message.answer(INTRO, reply_markup=value_menu_keyboard())

@router.callback_query(F.data == "vb_scan")
async def scan(call: CallbackQuery, db: AsyncSession):
    await call.answer("\u062f\u0631 \u062d\u0627\u0644 \u062c\u0633\u062a\u062c\u0648...")
    key = await ss.get_setting(db, "ODDS_API_KEY")
    if not key:
        await call.message.edit_text("\u26a0\ufe0f \u06a9\u0644\u06cc\u062f the-odds-api.com \u062a\u0646\u0638\u06cc\u0645 \u0646\u0634\u062f\u0647.\n\u0627\u0632 \u067e\u0646\u0644 \u2699\ufe0f \u062a\u0646\u0638\u06cc\u0645\u0627\u062a \u0648\u0627\u0631\u062f\u0634 \u06a9\u0646.", reply_markup=value_menu_keyboard()); return
    up = await dp.upcoming_matches(7); fin = await dp.finished_matches(90)
    preds = engine.predict_fixtures(up, fin, home_adv=ss.cfloat("HOME_ADV"), league_avg=ss.cfloat("LEAGUE_AVG"),
                                    rho=ss.cfloat("DC_RHO"), elo_weight=ss.cfloat("ELO_WEIGHT"), half_life=ss.cfloat("HALF_LIFE_DAYS"))
    odds = await vv.fetch_odds(key)
    vbs = vv.find_value_bets(preds, odds, min_edge=ss.cfloat("MIN_EDGE"), kelly_cap=ss.cfloat("KELLY_CAP"), kelly_mult=ss.cfloat("KELLY_MULT"))
    if not vbs:
        await call.message.edit_text("\u062f\u0631 \u062d\u0627\u0644 \u062d\u0627\u0636\u0631 \u0634\u0631\u0637 \u0627\u0631\u0632\u0634\u0645\u0646\u062f\u06cc \u067e\u06cc\u062f\u0627 \u0646\u0634\u062f.", reply_markup=value_menu_keyboard()); return
    bank = ss.cfloat("BANKROLL")
    lines = ["\U0001f4b0 <b>\u0634\u0631\u0637\u200c\u0647\u0627\u06cc \u0627\u0631\u0632\u0634\u0645\u0646\u062f</b>", ""]
    for v in vbs[:8]:
        stake = round(bank * v["kelly_stake_pct"] / 100, 2)
        lines.append(f"\u26bd <b>{v['home']} - {v['away']}</b>\n"
                     f"   \u2192 {v['selection_name']} | \u0636\u0631\u06cc\u0628 {v['odds']} | Edge {round(v['edge']*100,1)}%\n"
                     f"   \U0001f4b5 \u067e\u06cc\u0634\u0646\u0647\u0627\u062f Kelly: {v['kelly_stake_pct']}% (~{stake})")
    lines.append("\n\u26a0\ufe0f \u0628\u0627 \u0631\u06cc\u0633\u06a9 \u062e\u0648\u062f\u062a.")
    await call.message.edit_text("\n".join(lines), reply_markup=value_menu_keyboard())

@router.callback_query(F.data == "vb_stats")
async def vstats(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    s = await bs.stats(db, call.from_user.id)
    txt = (f"\U0001f4c8 <b>\u0622\u0645\u0627\u0631 \u0634\u0631\u0637\u200c\u0647\u0627\u06cc \u0645\u0646</b>\n\n"
           f"\u06a9\u0644: {s['total']} | \u062f\u0631\u0627\u0646\u062a\u0638\u0627\u0631: {s['pending']}\n"
           f"\u062a\u0633\u0648\u06cc\u0647: {s['settled']} | \u0628\u0631\u062f: {s['won']} ({s['win_rate']}%)\n"
           f"\u0634\u0631\u0637\u200c\u0628\u0633\u062a\u0647: {s['staked']} | \u0633\u0648\u062f: {s['profit']}\n"
           f"ROI: <b>{s['roi']}%</b>")
    await call.message.edit_text(txt, reply_markup=value_menu_keyboard())
