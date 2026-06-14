from aiogram import Router
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
    text = "<b>" + name + " خوش آمدید!</b>\n\nبه <b>ربات فوتبال</b> خوش آمدید!\n\nاز منوی زیر گزینه مورد نظر را انتخاب کنید:"
    await message.answer(text, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    lines = [
        "<b>راهنمای ربات فوتبال</b>",
        "",
        "/start - شروع",
        "/live - نتایج زنده",
        "/fixtures - برنامه بازی‌ها",
        "/predictions - پیش‌بینی‌ها",
        "/worldcup - جام جهانی 2026",
        "/stats - آمار",
        "/help - راهنما",
    ]
    await message.answer("\n".join(lines))
