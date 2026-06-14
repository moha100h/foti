from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="\U0001f534 \u0646\u062a\u0627\u06cc\u062c \u0632\u0646\u062f\u0647"),
         KeyboardButton(text="\U0001f4c5 \u0628\u0631\u0646\u0627\u0645\u0647 \u0628\u0627\u0632\u06cc\u200c\u0647\u0627")],
        [KeyboardButton(text="\U0001f3af \u067e\u06cc\u0634\u200c\u0628\u06cc\u0646\u06cc\u200c\u0647\u0627"),
         KeyboardButton(text="\U0001f3c6 \u062c\u0627\u0645 \u062c\u0647\u0627\u0646\u06cc \u06f2\u06f0\u06f2\u06f6")],
        [KeyboardButton(text="\U0001f4ca \u0622\u0645\u0627\u0631"),
         KeyboardButton(text="\u2139\ufe0f \u0631\u0627\u0647\u0646\u0645\u0627")],
    ], resize_keyboard=True)
