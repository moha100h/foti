from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def worldcup_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="جدول گروه‌ها", callback_data="wc_groups")],
        [InlineKeyboardButton(text="برنامه بازی‌ها", callback_data="wc_fixtures")],
        [InlineKeyboardButton(text="پیش‌بینی قهرمان", callback_data="wc_winner")],
        [InlineKeyboardButton(text="آمار تیم‌ها", callback_data="wc_teams")],
    ])
