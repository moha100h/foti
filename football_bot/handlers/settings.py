from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.config import settings
from football_bot.services import settings_service as ss, data_provider as dp
from football_bot.keyboards.settings_menu import settings_menu_keyboard, setting_edit_keyboard
router = Router()
NO = "\u062f\u0633\u062a\u0631\u0633\u06cc \u0646\u062f\u0627\u0631\u06cc."
class SetStates(StatesGroup):
    waiting_value = State()
def is_admin(uid): return uid in settings.ADMIN_IDS
def _mask(key, val):
    if key.endswith("TOKEN") or key.endswith("API_KEY"):
        if not val: return "\u062a\u0646\u0638\u06cc\u0645 \u0646\u0634\u062f\u0647"
        return (val[:4]+"..."+val[-4:]) if len(val)>=8 else "***"
    return val if val not in (None,"") else "-"
async def _stext(db):
    lines=["\u2699\ufe0f <b>\u062a\u0646\u0638\u06cc\u0645\u0627\u062a \u0628\u0627\u062a</b>",""]
    for key,(d,t,label) in ss.SCHEMA.items():
        lines.append(f"\u2022 {label}: <b>{_mask(key, await ss.get_setting(db,key))}</b>")
    lines+=["","\u0628\u0631\u0627\u06cc \u062a\u063a\u06cc\u06cc\u0631 \u0631\u0648\u06cc \u062f\u06a9\u0645\u0647 \u0628\u0632\u0646."]
    return "\n".join(lines)
@router.callback_query(F.data == "admin_settings")
async def open_s(call: CallbackQuery, db: AsyncSession, state: FSMContext):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    await state.clear(); await call.answer()
    try: await call.message.edit_text(await _stext(db), reply_markup=settings_menu_keyboard())
    except Exception: await call.message.answer(await _stext(db), reply_markup=settings_menu_keyboard())
@router.callback_query(F.data.startswith("set:"))
async def view_s(call: CallbackQuery, db: AsyncSession):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    key=call.data.split(":",1)[1]; d,t,label=ss.SCHEMA.get(key,("","str",key)); val=await ss.get_setting(db,key)
    await call.answer()
    await call.message.edit_text(f"\u2699\ufe0f <b>{label}</b>\n\n\u0645\u0642\u062f\u0627\u0631 \u0641\u0639\u0644\u06cc: <b>{_mask(key,val)}</b>\n\u067e\u06cc\u0634\u200c\u0641\u0631\u0636: <code>{d}</code>\n\u0646\u0648\u0639: {t}", reply_markup=setting_edit_keyboard(key))
@router.callback_query(F.data.startswith("setedit:"))
async def edit_s(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): await call.answer(NO,show_alert=True); return
    key=call.data.split(":",1)[1]; d,t,label=ss.SCHEMA.get(key,("","str",key))
    await state.set_state(SetStates.waiting_value); await state.update_data(key=key); await call.answer()
    hint="\u0639\u062f\u062f \u0627\u0639\u0634\u0627\u0631\u06cc" if t=="float" else "\u0645\u062a\u0646/\u06a9\u0644\u06cc\u062f"
    await call.message.answer(f"\u270f\ufe0f \u0645\u0642\u062f\u0627\u0631 \u062c\u062f\u06cc\u062f <b>{label}</b> \u0631\u0627 \u0628\u0641\u0631\u0633\u062a ({hint}).\n(\u062e\u0627\u0644\u06cc\u200c\u06a9\u0631\u062f\u0646: clear)")
@router.message(SetStates.waiting_value)
async def save_s(message: Message, state: FSMContext, db: AsyncSession):
    if not is_admin(message.from_user.id): await state.clear(); return
    key=(await state.get_data()).get("key"); d,t,label=ss.SCHEMA.get(key,("","str",key)); val=(message.text or "").strip()
    if val.lower()=="clear": val=""
    elif t=="float" and val:
        try: float(val)
        except ValueError: await message.answer("\u274c \u0628\u0627\u06cc\u062f \u0639\u062f\u062f \u0628\u0627\u0634\u062f."); return
    await ss.set_setting(db,key,val); dp._cache.clear(); await state.clear()
    await message.answer(f"\u2705 <b>{label}</b> \u0630\u062e\u06cc\u0631\u0647 \u0634\u062f.", reply_markup=settings_menu_keyboard())
