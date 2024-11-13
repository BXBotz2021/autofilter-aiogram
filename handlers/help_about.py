# handlers/help_about.py

from aiogram import types, Dispatcher

async def help_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("This is a movie bot. You can upload a movie file or type a movie name to search for it.")
    await callback_query.answer()

async def about_callback(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Developed by [Your Name].")
    await callback_query.answer()

def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(help_callback, lambda c: c.data == "help")
    dp.register_callback_query_handler(about_callback, lambda c: c.data == "about")
