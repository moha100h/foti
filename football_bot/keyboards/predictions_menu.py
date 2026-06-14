from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def predictions_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="اطمینان بالا", callback_data="pred_high")],
        [InlineKeyboardButton(text="اطمینان متوسط", callback_data="pred_medium")],
        [InlineKeyboardButton(text="آنالیز Over/Under", callback_data="pred_ou")],
        [InlineKeyboardButton(text="هر دو تیم گل بزنند", callback_data="pred_btts")],
    ])
