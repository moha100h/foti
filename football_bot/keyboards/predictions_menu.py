from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def predictions_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u0627\u0637\u0645\u06cc\u0646\u0627\u0646 \u0628\u0627\u0644\u0627", callback_data="pred_high")],
        [InlineKeyboardButton(text="\u0627\u0637\u0645\u06cc\u0646\u0627\u0646 \u0645\u062a\u0648\u0633\u0637", callback_data="pred_medium")],
        [InlineKeyboardButton(text="\u0622\u0646\u0627\u0644\u06cc\u0632 Over/Under", callback_data="pred_ou")],
        [InlineKeyboardButton(text="\u0647\u0631 \u062f\u0648 \u062a\u06cc\u0645 \u06af\u0644 \u0628\u0632\u0646\u0646\u062f", callback_data="pred_btts")],
    ])
