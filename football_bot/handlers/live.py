from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from football_bot.services import data_provider as dp
from football_bot.utils.formatting import fmt_live, FA
from football_bot.keyboards.live_menu import live_refresh_keyboard

router = Router()
LOADING = "\u062f\u0631 \u062d\u0627\u0644 \u062f\u0631\u06cc\u0627\u0641\u062a..."

async def _render():
    m = await dp.live_matches()
    if not m: return FA["no_live"]
    return FA["live_title"] + "".join(fmt_live(x) for x in m[:12])

@router.message(Command("live"))
@router.message(F.text == "\U0001f534 \u0646\u062a\u0627\u06cc\u062c \u0632\u0646\u062f\u0647")
async def cmd_live(message: Message):
    msg = await message.answer(LOADING)
    await msg.edit_text(await _render(), reply_markup=live_refresh_keyboard())

@router.callback_query(F.data == "refresh_live")
async def refresh(call: CallbackQuery):
    await call.answer("\u0628\u0647\u200c\u0631\u0648\u0632 \u0634\u062f")
    try:
        await call.message.edit_text(await _render(), reply_markup=live_refresh_keyboard())
    except Exception:
        pass
