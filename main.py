from db.db import SQLighter;
from env.api_token import API_TOKEN

from aiogram import Bot, Dispatcher, executor, types;

db = SQLighter("db/recept.db")

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands= ['start'])
async def welcome(message: types.Message):
    if (not db.is_user(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)

    db.add_subscription(message.from_user.id)
    

        
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


