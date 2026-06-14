from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from football_bot.services.prediction_service import get_high_confidence, get_medium_confidence
from football_bot.keyboards.predictions_menu import predictions_menu_keyboard
from football_bot.utils.formatting import format_prediction

router = Router()

MSG_SELECT = "نوع پیش‌بینی را انتخاب کنید:"
MSG_NO_HIGH = "پیش‌بینی با اطمینان بالا موجود نیست."
MSG_NO_MED = "پیش‌بینی با اطمینان متوسط موجود نیست."
MSG_HIGH_TITLE = "<b>پیش‌بینی‌های با اطمینان بالا</b>\n<i>بر اساس تحلیل آماری — تضمینی نیست</i>\n\n"
MSG_MED_TITLE = "<b>پیش‌بینی‌های با اطمینان متوسط</b>\n<i>بر اساس تحلیل آماری — تضمینی نیست</i>\n\n"


@router.message(Command("predictions"))
@router.message(F.text == "پیش‌بینی‌ها")
async def cmd_predictions(message: Message, db: AsyncSession):
    await message.answer(MSG_SELECT, reply_markup=predictions_menu_keyboard())


@router.callback_query(F.data == "pred_high")
async def pred_high(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    preds = await get_high_confidence(db)
    if not preds:
        await call.message.edit_text(MSG_NO_HIGH, reply_markup=predictions_menu_keyboard())
        return
    text = MSG_HIGH_TITLE + "".join(format_prediction(p) + "\n" for p in preds[:8])
    await call.message.edit_text(text, reply_markup=predictions_menu_keyboard())


@router.callback_query(F.data == "pred_medium")
async def pred_medium(call: CallbackQuery, db: AsyncSession):
    await call.answer()
    preds = await get_medium_confidence(db)
    if not preds:
        await call.message.edit_text(MSG_NO_MED, reply_markup=predictions_menu_keyboard())
        return
    text = MSG_MED_TITLE + "".join(format_prediction(p) + "\n" for p in preds[:8])
    await call.message.edit_text(text, reply_markup=predictions_menu_keyboard())
