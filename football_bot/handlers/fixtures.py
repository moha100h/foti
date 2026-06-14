from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from football_bot.services import data_provider as dp
from football_bot.utils.formatting import fmt_fixture
from football_bot.keyboards.fixtures_menu import fixtures_menu_keyboard

router = Router()
LOADING = "\u062f\u0631 \u062d\u0627\u0644 \u062f\u0631\u06cc\u0627\u0641\u062a..."
T_TODAY = "\U0001f4c5 <b>\u0628\u0627\u0632\u06cc\u200c\u0647\u0627\u06cc \u0627\u0645\u0631\u0648\u0632</b>\n\n"
T_TOMORROW = "\U0001f4c5 <b>\u0628\u0627\u0632\u06cc\u200c\u0647\u0627\u06cc \u0641\u0631\u062f\u0627</b>\n\n"
T_NONE = "\u0628\u0627\u0632\u06cc\u200c\u0627\u06cc \u06cc\u0627\u0641\u062a \u0646\u0634\u062f."

@router.message(Command("fixtures"))
@router.message(F.text == "\U0001f4c5 \u0628\u0631\u0646\u0627\u0645\u0647 \u0628\u0627\u0632\u06cc\u200c\u0647\u0627")
async def cmd_fixtures(message: Message):
    await message.answer("\u0631\u0648\u0632 \u0631\u0627 \u0627\u0646\u062a\u062e\u0627\u0628 \u06a9\u0646\u06cc\u062f:", reply_markup=fixtures_menu_keyboard())

async def _show(call, off, title):
    msg = await call.message.edit_text(LOADING)
    m = await dp.fixtures(off)
    if not m:
        await msg.edit_text(T_NONE, reply_markup=fixtures_menu_keyboard()); return
    await msg.edit_text(title + "".join(fmt_fixture(x) for x in m[:20]), reply_markup=fixtures_menu_keyboard())

@router.callback_query(F.data == "fixtures_today")
async def today(call: CallbackQuery):
    await call.answer(); await _show(call, 0, T_TODAY)

@router.callback_query(F.data == "fixtures_tomorrow")
async def tomorrow(call: CallbackQuery):
    await call.answer(); await _show(call, 1, T_TOMORROW)
