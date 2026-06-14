from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from football_bot.services.settings_service import SCHEMA
def settings_menu_keyboard():
    rows = [[InlineKeyboardButton(text=label, callback_data=f"set:{key}")] for key,(d,t,label) in SCHEMA.items()]
    rows.append([InlineKeyboardButton(text="\u2b05\ufe0f \u0628\u0627\u0632\u06af\u0634\u062a", callback_data="admin_home")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
def setting_edit_keyboard(key):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="\u270f\ufe0f \u062a\u063a\u06cc\u06cc\u0631 \u0645\u0642\u062f\u0627\u0631", callback_data=f"setedit:{key}")],[InlineKeyboardButton(text="\u2b05\ufe0f \u0628\u0627\u0632\u06af\u0634\u062a", callback_data="admin_settings")]])
