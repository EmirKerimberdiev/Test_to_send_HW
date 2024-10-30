from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from database.db import Database


token = dotenv_values(".env")['token']
bot = Bot(token=token)
dp = Dispatcher()
database = Database("db.sqlite3")