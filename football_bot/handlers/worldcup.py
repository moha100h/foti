from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.worldcup_service import get_wc_groups, get_wc_fixtures
from football_bot.keyboards.worldcup_menu import worldcup_menu_keyboard
from football_bot.utils.formatting import format_wc_match

router = Router()


@router.message(Command("worldcup"))
@router.message(F.text == "جام جهانی 2026")
async def cmd_worldcup(message: Message, db: AsyncSession):
    await message.answer("<b>جام جهانی 2026</b>

بخش مورد نظر را انتخاب کنید:", reply_markup=worldcup_menu_keyboard())


@router.callback_query(F.data == "wc_groups")
async def wc_groups(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    groups = await get_wc_groups(db)
    if not groups:
        await call.message.edit_text("اطلاعات گروه‌ها در دسترس نیست.", reply_markup=worldcup_menu_keyboard())
        return
    text = "<b>جدول گروه‌های جام جهانی 2026</b>

"
    for g in groups:
        text += f"<b>گروه {g['name']}</b>
"
        for t in g["teams"]:
            text += f"  {t['flag']} {t['name']} - {t['points']} امتیاز
"
        text += "
"
    await call.message.edit_text(text, reply_markup=worldcup_menu_keyboard())


@router.callback_query(F.data == "wc_fixtures")
async def wc_fixtures(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    matches = await get_wc_fixtures(db)
    if not matches:
        await call.message.edit_text("برنامه بازی‌ها در دسترس نیست.", reply_markup=worldcup_menu_keyboard())
        return
    text = "<b>بازی‌های جام جهانی 2026</b>

" + "".join(format_wc_match(m) + "
" for m in matches[:10])
    await call.message.edit_text(text, reply_markup=worldcup_menu_keyboard())
