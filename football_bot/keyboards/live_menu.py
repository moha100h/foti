from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def live_refresh_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="به‌روزرسانی", callback_data="refresh_live")]])
