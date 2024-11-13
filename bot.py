# bot.py

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from pymongo import MongoClient
import config
from handlers import start, movie_search, help_about

# Initialize bot and dispatcher with FSM storage
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# MongoDB setup
client = MongoClient(config.MONGO_URL)
db = client["movie_bot"]
movie_collection = db["movies"]

# Register handlers
start.register_handlers(dp)
movie_search.register_handlers(dp, movie_collection)
help_about.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
