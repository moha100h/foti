from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def worldcup_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\U0001f4c5 \u0628\u0627\u0632\u06cc\u200c\u0647\u0627", callback_data="wc_fixtures")],
        [InlineKeyboardButton(text="\U0001f3af \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc\u200c\u0647\u0627", callback_data="wc_preds")]])
