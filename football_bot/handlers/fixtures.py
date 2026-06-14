from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.fixtures_service import get_today_fixtures, get_tomorrow_fixtures
from football_bot.keyboards.fixtures_menu import fixtures_menu_keyboard
from football_bot.utils.formatting import format_fixture

router = Router()


@router.message(Command("fixtures"))
@router.message(F.text == "برنامه بازی‌ها")
async def cmd_fixtures(message: Message, db: AsyncSession):
    await message.answer("برنامه بازی‌ها را انتخاب کنید:", reply_markup=fixtures_menu_keyboard())


@router.callback_query(F.data == "fixtures_today")
async def fixtures_today(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    matches = await get_today_fixtures()
    if not matches:
        await call.message.edit_text("امروز بازی‌ای برنامه‌ریزی نشده.", reply_markup=fixtures_menu_keyboard())
        return
    text = "<b>بازی‌های امروز</b>

" + "".join(format_fixture(m) + "
" for m in matches[:15])
    await call.message.edit_text(text, reply_markup=fixtures_menu_keyboard())


@router.callback_query(F.data == "fixtures_tomorrow")
async def fixtures_tomorrow(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    matches = await get_tomorrow_fixtures()
    if not matches:
        await call.message.edit_text("فردا بازی‌ای برنامه‌ریزی نشده.", reply_markup=fixtures_menu_keyboard())
        return
    text = "<b>بازی‌های فردا</b>

" + "".join(format_fixture(m) + "
" for m in matches[:15])
    await call.message.edit_text(text, reply_markup=fixtures_menu_keyboard())
