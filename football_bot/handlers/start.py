from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.keyboards.main_menu import main_menu_keyboard
from football_bot.services.user_service import get_or_create_user
router = Router()
WELCOME = ("\U0001f3df\ufe0f <b>{name} \u062e\u0648\u0634 \u0622\u0645\u062f\u06cc!</b>\n\n\u0631\u0628\u0627\u062a \u062a\u062d\u0644\u06cc\u0644 \u0641\u0648\u062a\u0628\u0627\u0644 \u2014 Dixon-Coles\u060c \u0634\u0631\u0637 \u0627\u0631\u0632\u0634\u0645\u0646\u062f \u0648 \u0645\u062f\u06cc\u0631\u06cc\u062a \u0628\u0627\u0646\u06a9.\n\n\u0627\u0632 \u0645\u0646\u0648 \u0627\u0646\u062a\u062e\u0627\u0628 \u06a9\u0646:")
@router.message(CommandStart())
async def cmd_start(message: Message, db: AsyncSession, state: FSMContext):
    await state.clear()
    user = await get_or_create_user(db, message.from_user)
    await message.answer(WELCOME.format(name=user.first_name or ""), reply_markup=main_menu_keyboard())
@router.callback_query(F.data == "go_home")
async def go_home(call: CallbackQuery, state: FSMContext):
    await state.clear(); await call.answer()
    try: await call.message.delete()
    except Exception: pass
    await call.message.answer(WELCOME.format(name=call.from_user.first_name or ""), reply_markup=main_menu_keyboard())
@router.message(Command("help"))
@router.message(F.text == "\u2139\ufe0f \u0631\u0627\u0647\u0646\u0645\u0627")
async def cmd_help(message: Message):
    from football_bot.utils.help_text import HELP
    await message.answer(HELP)
