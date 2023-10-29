from db.db import SQLighter;
from env.api_token import API_TOKEN
from env.yookassa import YOO_API_TOKEN
from utils import *
from buttons import *

from aiogram import Bot, Dispatcher, executor, types;
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.message import ContentType
import json
import datetime
import random

db = SQLighter("db/recept.db")

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

data = {}

recepts = {
    'Завтраки': 'zavtraki',
    'Закуски': 'zakuski', 
    'Основные блюда': 'osnovnye-blyuda', 
    'Паста-Пицца': 'pasta-picca', 
    'Салаты': 'salaty', 
    'Супы': 'supy', 
    'Сендвичи': 'sendvichi', 
    'Выпечка-Десерты': 'vypechka-deserty',
    'zavtraki': 'Завтраки',
    'zakuski': 'Закуски', 
    'osnovnye-blyuda': 'Основные блюда', 
    'pasta-picca': 'Паста-Пицца', 
    'salaty': 'Салаты', 
    'supy': 'Супы', 
    'sendvichi': 'Сендвичи', 
    'vypechka-de serty': 'Выпечка-Десерты'
}

categories = ['Завтраки', 'Закуски', 'Основные блюда', 'Паста-Пицца', 'Салаты', 'Супы', 'Сендвичи', 'Выпечка-Десерты', 'Без разницы']

time_categories = {
    '20-25 минут': '0-25 минут',
    '25-50 минут': '25-50 минут',
    'более 50-60 минут': '50-600 минут',
    'Не имеет значения': '0-600 минут'
}

sub_days = {
    'sub_week': 7,
    'sub_month': 30,
    'sub_season': 90,
    'sub_half_year': 180
    }

@dp.message_handler(commands= ['start'])
async def def_welcome(message: types.Message):
    if (not db.is_user(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name) 
        db.add_start_subscription(message.from_user.id)
    sub = db.get_subscription(message.from_user.id)['data']

    if not sub['status']:
        await bot.send_message(message.from_user.id, "К сожалению, у вас закончилась подписка на бота😞\n\nДля того чтобы вновь получить доступ к более чем 2000 рецептам, продлите её, нажав на кнопку «Продлить🕓»", reply_markup=welcome(False))
        return

    if sub['description']['is_fulltime']:
        await bot.send_message(message.from_user.id, "У Вас бесконечная подписка", reply_markup=welcome(True))
        return
    if sub['description']['datetime_finaly']['is_current']:
        await bot.send_message(message.from_user.id, f"Подписка до: {sub['description']['datetime_finaly']['datetime']}", reply_markup=welcome(True))
        return
    if sub['description']['counter']:
        await bot.send_message(message.from_user.id, f"Количество оставшихся запросов: {sub['description']['counter']}", reply_markup=welcome(True))
        return

@dp.callback_query_handler(lambda callback: callback.data == 'menu')
async def def_menu(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Главное меню:', reply_markup=menu())

@dp.callback_query_handler(lambda callback: callback.data == 'lesson')
async def def_lesson(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, """
Для того чтобы получить доступ к более чем 2000 рецептам, Вам необходимо оформать подписку  

💻 Если вы ни разу не пользовались телеграмм ботом, не волнуйтесь. Он простой в использовании и быстро осваиваемый.

 1. Выберите из списка нужный Вам вид блюда (например завтрак).
 2. Затем выберите время приготовления.
 3. После этого выдаётся список блюд, подходящих под Ваши критерии.
 4. Кликаете на понравившееся и получаете подробный рецепт""", reply_markup=welcome(False))

@dp.message_handler(text='Вернуться в меню')
async def def_menu_message(message: types.Message):
    db.set_state_counter(message.from_user.id, 0)
    if db.get_subscription(message.from_user.id)['data']['status']:
        await bot.send_message(message.from_user.id, 'Главное меню:', reply_markup=menu())
    else: 
        await bot.send_message(message.from_user.id, 'К сожалению, у вас закончилась подписка на бота😞\n\nДля того чтобы вновь получить доступ к более чем 2000 рецептам, продлите её, нажав на кнопку «Продлить🕓»', reply_markup=welcome(False))

@dp.message_handler(text= 'Поиск рецептов🔎')
async def def_search_recepts(message: types.Message):
    db.set_state_counter(message.from_user.id, 0)
    if db.get_subscription(message.from_user.id)['data']['status']:
        await bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=search_recepts())
    else:
        await bot.send_message(message.from_user.id, 'К сожалению, у вас закончилась подписка на бота😞\n\nДля того чтобы вновь получить доступ к более чем 2000 рецептам, продлите её, нажав на кнопку «Продлить🕓»', reply_markup=welcome(False))

@dp.message_handler(text= categories)
async def def_time_to_dish(message: types.Message):
    if db.get_subscription(message.from_user.id)['data']['status']:
        if message.text != 'Без разницы': db.set_state_dish(message.from_user.id, recepts[message.text])
        else: db.set_state_dish(message.from_user.id, recepts[categories[random.randint(0, 7)]])
        await bot.send_message(message.from_user.id, 'Выберите время приготовления', reply_markup=time_to_dish())
    else:
        await bot.send_message(message.from_user.id, 'К сожалению, у вас закончилась подписка на бота😞\n\nДля того чтобы вновь получить доступ к более чем 2000 рецептам, продлите её, нажав на кнопку «Продлить🕓»', reply_markup=welcome(False))

@dp.message_handler(text= ['20-25 минут', '25-50 минут', 'более 50-60 минут', 'Не имеет значения'])
async def def_recept(message: types.Message):
    if db.get_subscription(message.from_user.id)['data']['status']:
        time = time_categories[message.text]
        db.set_state_time(message.from_user.id, time.split(' ')[0])
        await bot.send_message(message.from_user.id, f'Страница {db.get_state_counter(message.from_user.id) + 1}:', reply_markup=recepts_page(db.get_recepts_page(message.from_user.id)))
    else:
        await bot.send_message(message.from_user.id, 'К сожалению, у вас закончилась подписка на бота😞\n\nДля того чтобы вновь получить доступ к более чем 2000 рецептам, продлите её, нажав на кнопку «Продлить🕓»', reply_markup=welcome(False))

@dp.callback_query_handler(lambda callback: callback.data in ['next_page', 'prev_page'])
async def def_next_page(call: types.CallbackQuery):
    if call.data == 'next_page': 
        db.set_increment_page(call.from_user.id)
        page = db.get_recepts_page(call.from_user.id)
        if len(page) == 0:
            db.set_decrement_page(call.from_user.id)    
    else: db.set_decrement_page(call.from_user.id)
    try:
        await call.message.edit_text(f'Страница <b>{db.get_state_counter(call.from_user.id) + 1}</b>:', reply_markup=recepts_page(db.get_recepts_page(call.from_user.id)), parse_mode='HTML')
    except:
        pass

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("/recepty/"))
async def def_page_dish(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    sub = db.get_subscription(call.from_user.id)
    if sub['data']['status']:
        if not sub['data']['description']['is_fulltime'] or not sub['data']['description']['datetime_finaly']['is_current']: 
            db.decrement_counter_subscription(call.from_user.id)
        await bot.send_message(call.from_user.id, 'Ожидайте...')
        ingredients = db.get_ingredients(call.data)
        ingredients_string = '<b>Список Ингредиентов</b>\n' + '\n'.join([item[1] + ' : ' + item[2] for item in ingredients])
        
        instruction = data[call.data.split('/')[2]][call.data]['instructions']
        instruction_string = '\n\n<b>Рецепт</b>\n' + '\n\n'.join(item for item in instruction)

        photo = db.get_photo_dish(call.data.split('/')[2], call.data)

        try:
            if photo['img']: await bot.send_photo(call.from_user.id, photo=photo['img'], caption= (f'<b>{photo["name"]}</b>\n\n' + ingredients_string + instruction_string), reply_markup=menu(), parse_mode="HTML")
            else: await bot.send_message(call.from_user.id, f'<b>{photo["name"]}</b>\n\n' + ingredients_string + instruction_string, reply_markup=menu(), parse_mode="HTML")
        except:
            await bot.send_photo(call.from_user.id, photo=photo["img"])
            await bot.send_message(call.from_user.id, f'<b>{photo["name"]}</b>\n\n' + ingredients_string + instruction_string, reply_markup=menu(), parse_mode="HTML")
    else:
        await bot.send_message(call.from_user.id, 'К сожалению, у вас закончилась подписка на бота😞\n\nДля того чтобы вновь получить доступ к более чем 2000 рецептам, продлите её, нажав на кнопку «Продлить🕓»', reply_markup=welcome(False))

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'pay')
async def def_page_pay(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, '''
    <b>Стоимость подписки</b>
    7 дней    99.99₽   <s>159.99₽</s>
    30 дней    199.99₽  <s>459.99₽</s>
    90 дней    489.99₽  <s>959.99₽</s>
    180 дней    899.99₽  <s>1599.99₽</s>''', parse_mode="HTML", reply_markup=subscription())

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('sub_'))
async def def_sub(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    price = 9999
    if (call.data == 'sub_month'): price = 19999
    elif (call.data == 'sub_season'): price = 48999
    elif (call.data == 'sub_half_year'): price = 89999

    await bot.send_invoice(call.from_user.id, title='Оформление подписки', description='Подписка на более чем 2000 рецептов со всего мира', payload=call.data, provider_token=YOO_API_TOKEN, currency='RUB', start_parameter='test_bot', prices=[{'label': 'руб', 'amount': price}])

@dp.pre_checkout_query_handler()
async def pre_checkout_query_handler(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def def_process_pay(message: types.Message):
    db.set_subscription_time(message.from_user.id, datetime.datetime.now() + datetime.timedelta(days=sub_days[message.successful_payment.invoice_payload]))

    end_sub = db.get_subscription(message.from_user.id)['data']['description']['datetime_finaly']['datetime']
    await bot.send_message(message.from_user.id, f'<b>Успешно приобретена подписка на бота.</b>\nДата окончания подписки: {end_sub}', reply_markup=menu(), parse_mode='HTML')

    await bot.send_message(394248224, f'Пользователь {message.from_user.first_name} {message.from_user.last_name} (#{message.from_user.id}) приобрёл подписку!\n\nСрок: {sub_days[message.successful_payment.invoice_payload]} дней')

@dp.message_handler(text= 'Профиль💼')
async def def_profile(message: types.Message):
    profile = db.get_profile(message.from_user.id)
    sub = db.get_subscription(message.from_user.id)
    sub_str = 'Нет подписок'

    if sub['data']['status']:
        if sub['data']['description']['is_fulltime']:
            sub_str = 'Бесконечная'
        elif sub['data']['description']['datetime_finaly']['is_current']:
            sub_str = f"До {sub['data']['description']['datetime_finaly']['datetime']}"
        else:
            sub_str = f"{sub['data']['description']['counter']} рецепт"
            if sub['data']['description']['counter'] != 1:
                sub_str += 'а'

    await bot.send_message(message.from_user.id, f'''
<b>{profile[2]} {profile[3]}</b>
<b>Подписка</b>: {sub_str}

<b>telegram id:</b> {profile[1]}
<b>Дата регистрации:</b> {profile[4][:-7]}
<b>Последний запрос:</b> {recepts[profile[5]]}
    ''', parse_mode='HTML')

@dp.message_handler(text= 'Поддержка🤝')
async def def_support(message: types.Message):
    await bot.send_message(message.from_user.id, 'По всем вопросом обращайтесь @korotkovand', reply_markup=menu())

@dp.message_handler(text= 'Конструктор')
async def def_konstructor_ref(message: types.Message):
    await bot.send_message(message.from_user.id, '<b>Введите через запятую список имеющихся продуктов.</b>\n\nВаша корзина: ', reply_markup=basket(db.get_konstructor(message.from_user.id)), parse_mode='HTML')
    await bot.send_message(message.from_user.id, 'Для удаления продуктов, кликните на крестик рядом с нужным ингредиентом')

@dp.message_handler()
async def def_konstructor(message: types.Message):
    db.set_konstructor(message.from_user.id, [item.strip() for item in message.text.split(',')])
    await bot.send_message(message.from_user.id, "Ваша корзина продуктов:", reply_markup=basket(db.get_konstructor(message.from_user.id)))

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("/basket/"))
async def def_delete_ingredient(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    db.delete_ingredient(call.from_user.id, call.data[9:-1].split(',')[1][2:-1])
    await bot.send_message(call.from_user.id, "Ваша корзина продуктов:", reply_markup=basket(db.get_konstructor(call.from_user.id)))

@dp.callback_query_handler(lambda callback_query: callback_query.data in ['start_konstructor'])
async def def_start_konstructor(call: types.CallbackQuery):
    if db.get_subscription(call.from_user.id)['data']['status']:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await bot.send_message(call.from_user.id, 'Ожидайте...')
        urls = db.konstructor([ item[1] for item in db.get_konstructor(call.from_user.id)])
        if len(urls):
            page_dish = db.create_page_konstructor(urls)

            await bot.send_message(call.from_user.id, 'Выберите:', reply_markup=recepts_page(page_dish, False))
        else: 
            await bot.send_message(call.from_user.id, '''<b>К сожалению, мы не смогли найти рецепт для Вас...</b>
            
Вот наиболее часто встречающиеся ингредиенты для блюд:<b>
Соль
Молотый черный перец
Чеснок
Сливочное масло     
Сахар
Оливковое масло
Репчатый лук
Куриное яйцо
Вода
Помидоры
Растительное масло
Пшеничная мука
Морковь</b>
            
Добавьте ингредиенты из данного списка к себе в корзину и запустите консьруктор заново''', reply_markup=basket(db.get_konstructor(call.from_user.id)), parse_mode='HTML')
    
    else:
        await bot.send_message(call.from_user.id, 'К сожалению, у вас закончилась подписка на бота😞\n\nДля того чтобы вновь получить доступ к более чем 2000 рецептам, продлите её, нажав на кнопку «Продлить🕓»', reply_markup=welcome(False))

if __name__ == "__main__":
    with open('data/main_data.json', 'r', encoding='utf8') as file:
        data = json.load(file)
    print('DB is started...')
    print('Success to work...')
    executor.start_polling(dp, skip_updates=True)

    # db.most_popular_ingredients()        

    # print(db.konstructor(data = ['хлеб', 'Яйцо', 'молоко', 'бананы', 'кардамон']))