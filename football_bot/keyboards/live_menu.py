from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def live_refresh_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="\u0628\u0647\u200c\u0631\u0648\u0632\u0631\u0633\u0627\u0646\u06cc",
            callback_data="refresh_live",
        )],
    ])
