from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="نتایج زنده"), KeyboardButton(text="برنامه بازی‌ها")],
        [KeyboardButton(text="پیش‌بینی‌ها"), KeyboardButton(text="جام جهانی 2026")],
        [KeyboardButton(text="آمار"), KeyboardButton(text="راهنما")],
    ], resize_keyboard=True)
