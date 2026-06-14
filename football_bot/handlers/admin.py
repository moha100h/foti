from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from football_bot.config import settings
from football_bot.keyboards.admin_menu import admin_menu_keyboard
from football_bot.models.user import User
from football_bot.services import data_provider as dp, user_service as us
router = Router()
NO = "\u062f\u0633\u062a\u0631\u0633\u06cc \u0646\u062f\u0627\u0631\u06cc."
class AdminStates(StatesGroup):
    waiting_broadcast = State()
def is_admin(uid): return uid in settings.ADMIN_IDS
async def _ptext(db):
    n=await us.count_users(db)
    return f"\U0001f6e0\ufe0f <b>\u067e\u0646\u0644 \u0645\u062f\u06cc\u0631\u06cc\u062a</b>\n\n\U0001f465 \u06a9\u0627\u0631\u0628\u0631\u0627\u0646: <b>{n}</b>"
@router.message(Command("admin"))
async def cmd_admin(message: Message, db: AsyncSession, state: FSMContext):
    if not is_admin(message.from_user.id): await message.answer(NO); return
    await state.clear()
    await message.answer(await _ptext(db), reply_markup=admin_menu_keyboard())
@router.callback_query(F.data == "admin_home")
async def admin_home(call: CallbackQuery, db: AsyncSession, state: FSMContext):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    await state.clear(); await call.answer()
    try: await call.message.edit_text(await _ptext(db), reply_markup=admin_menu_keyboard())
    except Exception: await call.message.answer(await _ptext(db), reply_markup=admin_menu_keyboard())
@router.callback_query(F.data == "admin_refresh")
async def refresh(call: CallbackQuery, db: AsyncSession):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    dp._cache.clear(); await call.answer("\u06a9\u0634 \u067e\u0627\u06a9 \u0634\u062f \u2714\ufe0f", show_alert=True)
@router.callback_query(F.data == "admin_broadcast")
async def ask_b(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    await call.answer(); await state.set_state(AdminStates.waiting_broadcast)
    await call.message.answer("\U0001f4e2 \u067e\u06cc\u0627\u0645 \u0647\u0645\u06af\u0627\u0646\u06cc \u0631\u0627 \u0628\u0646\u0648\u06cc\u0633:")
@router.message(AdminStates.waiting_broadcast)
async def do_b(message: Message, state: FSMContext, db: AsyncSession):
    if not is_admin(message.from_user.id): await state.clear(); return
    await state.clear()
    res=await db.execute(select(User.telegram_id).where(User.is_banned == False))
    ok=0
    for (uid,) in res.all():
        try: await message.bot.send_message(uid, message.text or ""); ok+=1
        except Exception: pass
    await message.answer(f"\u2705 \u0627\u0631\u0633\u0627\u0644 \u0628\u0647 {ok} \u06a9\u0627\u0631\u0628\u0631.", reply_markup=admin_menu_keyboard())
