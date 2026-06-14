from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.config import settings
from football_bot.services import user_service as us
from football_bot.keyboards.admin_menu import users_menu_keyboard
router = Router()
NO = "\u062f\u0633\u062a\u0631\u0633\u06cc \u0646\u062f\u0627\u0631\u06cc."
class UserStates(StatesGroup):
    adding = State(); removing = State()
def is_admin(uid): return uid in settings.ADMIN_IDS
@router.callback_query(F.data == "admin_users")
async def open_u(call: CallbackQuery, db: AsyncSession, state: FSMContext):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    await state.clear(); await call.answer()
    n=await us.count_users(db)
    await call.message.edit_text(f"\U0001f465 <b>\u0645\u062f\u06cc\u0631\u06cc\u062a \u06a9\u0627\u0631\u0628\u0631\u0627\u0646</b>\n\n\u0645\u062c\u0645\u0648\u0639: <b>{n}</b>", reply_markup=users_menu_keyboard())
@router.callback_query(F.data == "user_add")
async def ask_a(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    await state.set_state(UserStates.adding); await call.answer()
    await call.message.answer("\u2795 \u0622\u06cc\u062f\u06cc \u0639\u062f\u062f\u06cc \u06a9\u0627\u0631\u0628\u0631 (+ \u0627\u062e\u062a\u06cc\u0627\u0631\u06cc \u0646\u0627\u0645).\n\u0645\u062b\u0627\u0644: <code>123456789 Ali</code>")
@router.message(UserStates.adding)
async def do_a(message: Message, state: FSMContext, db: AsyncSession):
    if not is_admin(message.from_user.id): await state.clear(); return
    parts=(message.text or "").split(maxsplit=1)
    if not parts or not parts[0].lstrip("-").isdigit(): await message.answer("\u274c \u0622\u06cc\u062f\u06cc \u0639\u062f\u062f\u06cc \u0645\u0639\u062a\u0628\u0631 \u0628\u0641\u0631\u0633\u062a."); return
    uid=int(parts[0]); name=parts[1] if len(parts)>1 else ""
    await us.add_user_manual(db,uid,name); await state.clear()
    await message.answer(f"\u2705 \u06a9\u0627\u0631\u0628\u0631 <code>{uid}</code> \u0627\u0636\u0627\u0641\u0647 \u0634\u062f.", reply_markup=users_menu_keyboard())
@router.callback_query(F.data == "user_del")
async def ask_d(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    await state.set_state(UserStates.removing); await call.answer()
    await call.message.answer("\u2796 \u0622\u06cc\u062f\u06cc \u0639\u062f\u062f\u06cc \u06a9\u0627\u0631\u0628\u0631 \u0628\u0631\u0627\u06cc \u062d\u0630\u0641.")
@router.message(UserStates.removing)
async def do_d(message: Message, state: FSMContext, db: AsyncSession):
    if not is_admin(message.from_user.id): await state.clear(); return
    txt=(message.text or "").strip()
    if not txt.lstrip("-").isdigit(): await message.answer("\u274c \u0622\u06cc\u062f\u06cc \u0639\u062f\u062f\u06cc \u0645\u0639\u062a\u0628\u0631 \u0628\u0641\u0631\u0633\u062a."); return
    ok=await us.remove_user(db,int(txt)); await state.clear()
    await message.answer("\u2705 \u0627\u0646\u062c\u0627\u0645 \u0634\u062f." if ok else "\u26a0\ufe0f \u067e\u06cc\u062f\u0627 \u0646\u0634\u062f.", reply_markup=users_menu_keyboard())
@router.callback_query(F.data == "user_list")
async def list_u(call: CallbackQuery, db: AsyncSession):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    await call.answer(); users=await us.list_users(db,30)
    if not users: await call.message.edit_text("\u06a9\u0627\u0631\u0628\u0631\u06cc \u0646\u06cc\u0633\u062a.", reply_markup=users_menu_keyboard()); return
    lines=["\U0001f4cb <b>\u06a9\u0627\u0631\u0628\u0631\u0627\u0646 \u0627\u062e\u06cc\u0631</b>",""]
    for u in users:
        tag=("@"+u.username) if u.username else (u.first_name or "-")
        lines.append(f"{'\u26d4' if u.is_banned else '\u2705'} <code>{u.telegram_id}</code> {tag}")
    await call.message.edit_text("\n".join(lines), reply_markup=users_menu_keyboard())
