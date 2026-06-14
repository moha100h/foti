from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def worldcup_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u062c\u062f\u0648\u0644 \u06af\u0631\u0648\u0647\u200c\u0647\u0627", callback_data="wc_groups")],
        [InlineKeyboardButton(text="\u0628\u0631\u0646\u0627\u0645\u0647 \u0628\u0627\u0632\u06cc\u200c\u0647\u0627", callback_data="wc_fixtures")],
        [InlineKeyboardButton(text="\u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc \u0642\u0647\u0631\u0645\u0627\u0646", callback_data="wc_winner")],
        [InlineKeyboardButton(text="\u0622\u0645\u0627\u0631 \u062a\u06cc\u0645\u200c\u0647\u0627", callback_data="wc_teams")],
    ])
