from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def live_refresh_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="\U0001f504 \u0628\u0647\u200c\u0631\u0648\u0632\u0631\u0633\u0627\u0646\u06cc", callback_data="refresh_live")],[InlineKeyboardButton(text="\u2b05\ufe0f \u0628\u0627\u0632\u06af\u0634\u062a", callback_data="go_home")]])
