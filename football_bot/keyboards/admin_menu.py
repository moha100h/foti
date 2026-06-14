from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ارسال پیام همگانی", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="وضعیت سیستم", callback_data="admin_status")],
        [InlineKeyboardButton(text="لاگ‌های خطا", callback_data="admin_errors")],
    ])
