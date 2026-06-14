from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\U0001f511 \u062a\u0646\u0638\u06cc\u0645 \u06a9\u0644\u06cc\u062f API", callback_data="admin_set_api")],
        [InlineKeyboardButton(text="\U0001f4e2 \u067e\u06cc\u0627\u0645 \u0647\u0645\u06af\u0627\u0646\u06cc", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="\U0001f504 \u062a\u0627\u0632\u0647\u200c\u0633\u0627\u0632\u06cc \u062f\u0627\u062f\u0647\u200c\u0647\u0627", callback_data="admin_refresh")],
    ])
