from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\U0001f4e2 \u067e\u06cc\u0627\u0645 \u0647\u0645\u06af\u0627\u0646\u06cc", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="\U0001f504 \u062a\u0627\u0632\u0647\u200c\u0633\u0627\u0632\u06cc", callback_data="admin_refresh")]])
