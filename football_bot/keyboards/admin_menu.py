from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\u0627\u0631\u0633\u0627\u0644 \u067e\u06cc\u0627\u0645 \u0647\u0645\u06af\u0627\u0646\u06cc", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="\u0648\u0636\u0639\u06cc\u062a \u0633\u06cc\u0633\u062a\u0645", callback_data="admin_status")],
        [InlineKeyboardButton(text="\u0644\u0627\u06af\u200c\u0647\u0627\u06cc \u062e\u0637\u0627", callback_data="admin_errors")],
    ])
