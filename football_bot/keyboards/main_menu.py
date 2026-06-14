from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="\u0646\u062a\u0627\u06cc\u062c \u0632\u0646\u062f\u0647"),
                KeyboardButton(text="\u0628\u0631\u0646\u0627\u0645\u0647 \u0628\u0627\u0632\u06cc\u200c\u0647\u0627"),
            ],
            [
                KeyboardButton(text="\u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc\u200c\u0647\u0627"),
                KeyboardButton(text="\u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc 2026"),
            ],
            [
                KeyboardButton(text="\u0622\u0645\u0627\u0631"),
                KeyboardButton(text="\u0631\u0627\u0647\u0646\u0645\u0627"),
            ],
        ],
        resize_keyboard=True,
    )
