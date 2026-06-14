from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.worldcup_service import get_wc_groups, get_wc_fixtures
from football_bot.keyboards.worldcup_menu import worldcup_menu_keyboard
from football_bot.utils.formatting import format_wc_match

router = Router()

MSG_WELCOME = "<b>جام جهانی 2026</b>\n\nبخش مورد نظر را انتخاب کنید:"
MSG_NO_GROUPS = "اطلاعات گروه‌ها در دسترس نیست."
MSG_NO_FIXTURES = "برنامه بازی‌ها در دسترس نیست."
MSG_GROUPS_TITLE = "<b>جدول گروه‌های جام جهانی 2026</b>\n\n"
MSG_FIXTURES_TITLE = "<b>بازی‌های جام جهانی 2026</b>\n\n"


@router.message(Command("worldcup"))
@router.message(F.text == "جام جهانی 2026")
async def cmd_worldcup(message: Message, db: AsyncSession):
    await message.answer(MSG_WELCOME, reply_markup=worldcup_menu_keyboard())


@router.callback_query(F.data == "wc_groups")
async def wc_groups(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    groups = await get_wc_groups(db)
    if not groups:
        await call.message.edit_text(MSG_NO_GROUPS, reply_markup=worldcup_menu_keyboard())
        return
    lines = [MSG_GROUPS_TITLE]
    for g in groups:
        lines.append("<b>" + "گروه " + g["name"] + "</b>\n")
        for t in g["teams"]:
            lines.append("  " + t["flag"] + " " + t["name"] + " - " + str(t["points"]) + " امتیاز\n")
        lines.append("\n")
    await call.message.edit_text("".join(lines), reply_markup=worldcup_menu_keyboard())


@router.callback_query(F.data == "wc_fixtures")
async def wc_fixtures(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    matches = await get_wc_fixtures(db)
    if not matches:
        await call.message.edit_text(MSG_NO_FIXTURES, reply_markup=worldcup_menu_keyboard())
        return
    text = MSG_FIXTURES_TITLE + "".join(format_wc_match(m) + "\n" for m in matches[:10])
    await call.message.edit_text(text, reply_markup=worldcup_menu_keyboard())
