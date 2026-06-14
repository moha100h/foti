from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def stats_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="\u26bd \u0628\u0631\u062a\u0631\u06cc\u0646 \u06af\u0644\u0632\u0646\u0627\u0646", callback_data="stats_scorers")],[InlineKeyboardButton(text="\U0001f4cb \u062c\u062f\u0648\u0644 \u0644\u06cc\u06af", callback_data="stats_table")],[InlineKeyboardButton(text="\u2b05\ufe0f \u0628\u0627\u0632\u06af\u0634\u062a", callback_data="go_home")]])
