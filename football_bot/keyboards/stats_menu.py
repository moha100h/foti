from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def stats_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="برترین گلزنان", callback_data="stats_scorers")],
        [InlineKeyboardButton(text="برترین پاس‌دهندگان", callback_data="stats_assists")],
        [InlineKeyboardButton(text="جدول لیگ", callback_data="stats_table")],
    ])
