from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.keyboards.main_menu import main_menu_keyboard
from football_bot.services.user_service import get_or_create_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, db: AsyncSession):
    user = await get_or_create_user(db, message.from_user)
    name = user.first_name or ""
    text = ("\U0001f3df\ufe0f <b>" + name + " \u062e\u0648\u0634 \u0622\u0645\u062f\u06cc\u062f!</b>\n\n"
            "\u0628\u0647 <b>\u0631\u0628\u0627\u062a \u0641\u0648\u062a\u0628\u0627\u0644</b> \u062e\u0648\u0634 \u0622\u0645\u062f\u06cc\u062f!\n"
            "\u0646\u062a\u0627\u06cc\u062c \u0632\u0646\u062f\u0647\u060c \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc \u0647\u0648\u0634\u0645\u0646\u062f \u0648 \u0622\u0645\u0627\u0631.\n\n"
            "\u0627\u0632 \u0645\u0646\u0648\u06cc \u0632\u06cc\u0631 \u0627\u0646\u062a\u062e\u0627\u0628 \u06a9\u0646\u06cc\u062f:")
    await message.answer(text, reply_markup=main_menu_keyboard())

@router.message(Command("help"))
@router.message(F.text == "\u2139\ufe0f \u0631\u0627\u0647\u0646\u0645\u0627")
async def cmd_help(message: Message):
    lines = ["<b>\U0001f4d6 \u0631\u0627\u0647\u0646\u0645\u0627</b>", "",
             "\U0001f534 /live", "\U0001f4c5 /fixtures", "\U0001f3af /predictions",
             "\U0001f3c6 /worldcup", "\U0001f4ca /stats"]
    await message.answer("\n".join(lines))
