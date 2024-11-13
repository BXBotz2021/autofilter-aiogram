# handlers/start.py

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Help", callback_data="help"),
        InlineKeyboardButton("About", callback_data="about")
    )
    await message.answer("Welcome to the Movie Bot! You can upload and search for movies here.", reply_markup=keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
