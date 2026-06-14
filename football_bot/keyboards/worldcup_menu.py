from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def worldcup_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="\U0001f534 \u0628\u0627\u0632\u06cc\u200c\u0647\u0627\u06cc \u0632\u0646\u062f\u0647", callback_data="wc_live")],[InlineKeyboardButton(text="\U0001f4c5 \u0628\u0627\u0632\u06cc\u200c\u0647\u0627", callback_data="wc_fixtures"),InlineKeyboardButton(text="\U0001f3af \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc\u200c\u0647\u0627", callback_data="wc_preds")],[InlineKeyboardButton(text="\u2b05\ufe0f \u0628\u0627\u0632\u06af\u0634\u062a", callback_data="go_home")]])
def wc_live_refresh_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="\U0001f504 \u0628\u0647\u200c\u0631\u0648\u0632\u0631\u0633\u0627\u0646\u06cc", callback_data="wc_live")],[InlineKeyboardButton(text="\u2b05\ufe0f \u0628\u0627\u0632\u06af\u0634\u062a", callback_data="wc_back")]])
