from db.db import SQLighter;
from env.api_token import API_TOKEN
from utils import *
from buttons import *

from aiogram import Bot, Dispatcher, executor, types;
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

db = SQLighter("db/recept.db")

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands= ['start'])
async def welcome(message: types.Message):
    if (not db.is_user(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    await bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}😇", reply_markup=check_sub(db.is_subscription(message.from_user.id)))
    db.add_subscription(message.from_user.id)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)