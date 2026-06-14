from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def stats_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u0628\u0631\u062a\u0631\u06cc\u0646 \u06af\u0644\u0632\u0646\u0627\u0646", callback_data="stats_scorers")],
        [InlineKeyboardButton(text="\u0628\u0631\u062a\u0631\u06cc\u0646 \u067e\u0627\u0633\u200c\u062f\u0647\u0646\u062f\u06af\u0627\u0646", callback_data="stats_assists")],
        [InlineKeyboardButton(text="\u062c\u062f\u0648\u0644 \u0644\u06cc\u06af", callback_data="stats_table")],
    ])
