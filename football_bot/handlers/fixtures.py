from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.fixtures_service import get_today_fixtures, get_tomorrow_fixtures
from football_bot.keyboards.fixtures_menu import fixtures_menu_keyboard
from football_bot.utils.formatting import format_fixture

router = Router()

MSG_SELECT = "برنامه بازی‌ها را انتخاب کنید:"
MSG_NO_TODAY = "امروز بازیای برنامه‌ریزی نشده."
MSG_NO_TOMORROW = "فردا بازیای برنامه‌ریزی نشده."
MSG_TODAY = "<b>بازی‌های امروز</b>\n\n"
MSG_TOMORROW = "<b>بازی‌های فردا</b>\n\n"


@router.message(Command("fixtures"))
@router.message(F.text == "برنامه بازی‌ها")
async def cmd_fixtures(message: Message, db: AsyncSession):
    await message.answer(MSG_SELECT, reply_markup=fixtures_menu_keyboard())


@router.callback_query(F.data == "fixtures_today")
async def fixtures_today(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    matches = await get_today_fixtures()
    if not matches:
        await call.message.edit_text(MSG_NO_TODAY, reply_markup=fixtures_menu_keyboard())
        return
    text = MSG_TODAY + "".join(format_fixture(m) + "\n" for m in matches[:15])
    await call.message.edit_text(text, reply_markup=fixtures_menu_keyboard())


@router.callback_query(F.data == "fixtures_tomorrow")
async def fixtures_tomorrow(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    matches = await get_tomorrow_fixtures()
    if not matches:
        await call.message.edit_text(MSG_NO_TOMORROW, reply_markup=fixtures_menu_keyboard())
        return
    text = MSG_TOMORROW + "".join(format_fixture(m) + "\n" for m in matches[:15])
    await call.message.edit_text(text, reply_markup=fixtures_menu_keyboard())
