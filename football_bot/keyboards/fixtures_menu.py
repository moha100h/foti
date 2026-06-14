from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def fixtures_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="\u0627\u0645\u0631\u0648\u0632", callback_data="fixtures_today"),
            InlineKeyboardButton(text="\u0641\u0631\u062f\u0627", callback_data="fixtures_tomorrow"),
        ],
        [InlineKeyboardButton(text="\u0627\u06cc\u0646 \u0647\u0641\u062a\u0647", callback_data="fixtures_week")],
    ])
