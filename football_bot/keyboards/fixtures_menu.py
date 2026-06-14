from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def fixtures_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u0627\u0645\u0631\u0648\u0632", callback_data="fixtures_today"),
         InlineKeyboardButton(text="\u0641\u0631\u062f\u0627", callback_data="fixtures_tomorrow")]])
