from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from football_bot.config import settings
from football_bot.keyboards.admin_menu import admin_menu_keyboard
from football_bot.models.user import User
from football_bot.services import settings_service, data_provider as dp

router = Router()
NO_ACCESS = "\u062f\u0633\u062a\u0631\u0633\u06cc \u0646\u062f\u0627\u0631\u06cc\u062f."


class AdminStates(StatesGroup):
    waiting_api_key = State()
    waiting_broadcast = State()


def is_admin(uid):
    return uid in settings.ADMIN_IDS


async def _panel_text(db: AsyncSession) -> str:
    users = await db.scalar(select(func.count(User.telegram_id)))
    tok = settings_service.cache_get("FOOTBALL_DATA_TOKEN") or getattr(settings, "FOOTBALL_DATA_TOKEN", "") or ""
    masked = (tok[:4] + "..." + tok[-4:]) if len(tok) >= 8 else ("\u0646\u0627\u0645\u0639\u062a\u0628\u0631" if tok else "\u062a\u0646\u0638\u06cc\u0645 \u0646\u0634\u062f\u0647")
    return ("\U0001f6e0\ufe0f <b>\u067e\u0646\u0644 \u0645\u062f\u06cc\u0631\u06cc\u062a</b>\n\n"
            "\U0001f465 \u06a9\u0627\u0631\u0628\u0631\u0627\u0646: <b>" + str(users or 0) + "</b>\n"
            "\U0001f511 \u06a9\u0644\u06cc\u062f API: <b>" + masked + "</b>")


@router.message(Command("admin"))
async def cmd_admin(message: Message, db: AsyncSession):
    if not is_admin(message.from_user.id):
        await message.answer(NO_ACCESS); return
    await message.answer(await _panel_text(db), reply_markup=admin_menu_keyboard())


@router.callback_query(F.data == "admin_refresh")
async def refresh(call: CallbackQuery, db: AsyncSession):
    if not is_admin(call.from_user.id):
        await call.answer(NO_ACCESS, show_alert=True); return
    dp._cache.clear()
    await call.answer("\u06a9\u0634 \u067e\u0627\u06a9 \u0634\u062f \u2714\ufe0f", show_alert=True)
    try:
        await call.message.edit_text(await _panel_text(db), reply_markup=admin_menu_keyboard())
    except Exception:
        pass


@router.callback_query(F.data == "admin_set_api")
async def ask_api(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer(NO_ACCESS, show_alert=True); return
    await call.answer()
    await state.set_state(AdminStates.waiting_api_key)
    await call.message.answer(
        "\U0001f511 \u06a9\u0644\u06cc\u062f API \u0633\u0627\u06cc\u062a football-data.org \u0631\u0627 \u0628\u0641\u0631\u0633\u062a\u06cc\u062f.\n"
        "(\u0628\u0631\u0627\u06cc \u062d\u0630\u0641 \u06a9\u0644\u06cc\u062f \u0639\u0628\u0627\u0631\u062a clear \u0631\u0627 \u0628\u0641\u0631\u0633\u062a\u06cc\u062f)"
    )


@router.message(AdminStates.waiting_api_key)
async def save_api(message: Message, state: FSMContext, db: AsyncSession):
    if not is_admin(message.from_user.id):
        await state.clear(); return
    val = (message.text or "").strip()
    if val.lower() == "clear":
        val = ""
    await settings_service.set_setting(db, "FOOTBALL_DATA_TOKEN", val)
    dp._cache.clear()
    await state.clear()
    await message.answer("\u2705 \u06a9\u0644\u06cc\u062f API \u0630\u062e\u06cc\u0631\u0647 \u0634\u062f \u0648 \u06a9\u0634 \u067e\u0627\u06a9 \u0634\u062f.",
                         reply_markup=admin_menu_keyboard())


@router.callback_query(F.data == "admin_broadcast")
async def ask_broadcast(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer(NO_ACCESS, show_alert=True); return
    await call.answer()
    await state.set_state(AdminStates.waiting_broadcast)
    await call.message.answer("\U0001f4e2 \u067e\u06cc\u0627\u0645 \u0647\u0645\u06af\u0627\u0646\u06cc \u0631\u0627 \u0628\u0646\u0648\u06cc\u0633\u06cc\u062f:")


@router.message(AdminStates.waiting_broadcast)
async def do_broadcast(message: Message, state: FSMContext, db: AsyncSession):
    if not is_admin(message.from_user.id):
        await state.clear(); return
    await state.clear()
    res = await db.execute(select(User.telegram_id))
    ids = [r[0] for r in res.all()]
    ok = 0
    for uid in ids:
        try:
            await message.bot.send_message(uid, message.text or "")
            ok += 1
        except Exception:
            pass
    await message.answer("\u2705 \u0627\u0631\u0633\u0627\u0644 \u0634\u062f \u0628\u0647 " + str(ok) + " \u06a9\u0627\u0631\u0628\u0631.",
                         reply_markup=admin_menu_keyboard())
