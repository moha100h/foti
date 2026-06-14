from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def fixtures_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="امروز", callback_data="fixtures_today"), InlineKeyboardButton(text="فردا", callback_data="fixtures_tomorrow")],
        [InlineKeyboardButton(text="این هفته", callback_data="fixtures_week")],
    ])
