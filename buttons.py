from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def welcome(is_sub = False):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    b_to_pay = KeyboardButton(text = 'Продлить🕓', callback_data = 'pay')
    b_to_lesson = KeyboardButton(text = 'Инструкция', callback_data = 'lesson')
    if not is_sub: return keyboard.add(b_to_pay, b_to_lesson)

    b_to_bot = KeyboardButton(text = 'Перейти к боту', callback_data = 'menu')
    return keyboard.add(b_to_bot)

def menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    b_search = KeyboardButton(text = 'Поиск рецептов🔎')
    b_profile = KeyboardButton(text = 'Профиль💼')
    b_support = KeyboardButton(text = 'Поддержка🤝')
    # b_konstructor = KeyboardButton(text = 'Конструктор')
    # return keyboard.add(b_search, b_profile).add(b_support).add(b_konstructor)
    return keyboard.add(b_search, b_profile).add(b_support)

def search_recepts():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    b_zavtraki = KeyboardButton(text = 'Завтраки')
    b_zakuski = KeyboardButton(text = 'Закуски')
    b_osnovnye_blyuda = KeyboardButton(text = 'Основные блюда')
    b_pasta_picca = KeyboardButton(text = 'Паста-Пицца')
    b_salaty = KeyboardButton(text = 'Салаты')
    b_supy = KeyboardButton(text = 'Супы')
    b_sendvichi = KeyboardButton(text = 'Сендвичи')
    b_vypechka_deserty = KeyboardButton(text = 'Выпечка-Десерты')
    b_all = KeyboardButton(text = 'Без разницы')
    b_back_menu = KeyboardButton(text = 'Вернуться в меню')
    return keyboard.add(b_zavtraki, b_zakuski).add(b_osnovnye_blyuda, b_pasta_picca).add(b_salaty, b_supy).add(b_sendvichi, b_vypechka_deserty).add(b_all).add(b_back_menu)

def time_to_dish(): 
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    b_1 = KeyboardButton(text = '20-25 минут')
    b_2 = KeyboardButton(text = '25-50 минут')
    b_3 = KeyboardButton(text = 'более 50-60 минут')
    b_all = KeyboardButton(text = 'Не имеет значения')
    b_back_menu = KeyboardButton(text = 'Вернуться в меню')
    return keyboard.add(b_1).add(b_2).add(b_3).add(b_all).add(b_back_menu)

def recepts_page(recepts_list, is_page=True):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    for item in recepts_list:
        keyboard.add(KeyboardButton(text = f'{item[1]}', callback_data = f'{item[-2]}'))

    if not is_page: return keyboard

    b_next = KeyboardButton(text = '➡️', callback_data = 'next_page')
    b_prev = KeyboardButton(text = '⬅️', callback_data = 'prev_page')
    return keyboard.add(b_prev, b_next)

def basket(ingredients):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    for item in ingredients:
        keyboard.add(KeyboardButton(text = f'{item[1]}  ✖', callback_data = f'/basket/ {item}'))
    
    b_start_konstructor = KeyboardButton(text = 'Подобрать рецепт ✅', callback_data = 'start_konstructor') 
    return keyboard.add(b_start_konstructor)

def subscription():
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    b_sub_week = KeyboardButton(text = '7 дней', callback_data = 'sub_week') 
    b_sub_month = KeyboardButton(text = '30 дней', callback_data = 'sub_month') 
    b_sub_season = KeyboardButton(text = '90 дней', callback_data = 'sub_season') 
    b_sub_half_year = KeyboardButton(text = '180 дней', callback_data = 'sub_half_year') 
    return keyboard.add(b_sub_week, b_sub_month, b_sub_season, b_sub_half_year)