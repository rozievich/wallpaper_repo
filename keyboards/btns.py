from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


def main_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    btn.add(KeyboardButton('Top 🔝'), KeyboardButton('Dasturchiga xabar 💬'))
    return btn


def exit_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    btn.add(KeyboardButton('❌'))
    return btn


def admin_btn():
    btn = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    btn.add(KeyboardButton('📊 Statistika'), KeyboardButton("🗣 Reklama"), KeyboardButton('Back ⬅️'))
    return btn
