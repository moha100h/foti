from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def predictions_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\U0001f525 \u0628\u0647\u062a\u0631\u06cc\u0646 \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc\u200c\u0647\u0627", callback_data="pred_top")],
        [InlineKeyboardButton(text="\u26bd \u0628\u0627\u0644\u0627\u06cc \u06f2.\u06f5", callback_data="pred_ou"),
         InlineKeyboardButton(text="\U0001f3af \u0647\u0631\u062f\u0648 \u06af\u0644", callback_data="pred_btts")]])
