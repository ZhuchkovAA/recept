from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def check_sub(is_sub = False):
    keyboard = InlineKeyboardMarkup()
    b_to_pay = KeyboardButton(text = 'Продлить🕓', callback_data = 'to_pay')
    b_to_bot = KeyboardButton(text = 'Перейти к боту', callback_data = 'menu')
    if is_sub: return keyboard.add(b_to_pay, b_to_bot)
    b_to_lesson = KeyboardButton(text = 'Инструкция', callback_data='to_lesson')
    return keyboard.add(b_to_pay, b_to_lesson)

def menu():
    keyboard = InlineKeyboardMarkup()
    b_search = KeyboardButton(text = 'Поиск рецептов🔎', callback_data = 'search')
    b_profile = KeyboardButton(text = 'Профиль💼', callback_data = 'profile')
    b_support = KeyboardButton(text = 'Поддержка🤝', callback_data = 'support')
    return keyboard.add(b_search, b_profile).add(b_support)