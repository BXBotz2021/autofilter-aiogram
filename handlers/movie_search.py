# handlers/movie_search.py

from aiogram import types, Dispatcher
from pymongo.collection import Collection
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class UploadMovie(StatesGroup):
    waiting_for_movie_name = State()

async def handle_file_upload(message: types.Message, state: FSMContext, movie_collection: Collection):
    file_id = None
    file_type = None

    # Determine file type and get file ID
    if message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.video:
        file_id = message.video.file_id
        file_type = "video"
    else:
        await message.reply("Please upload a valid document or video file.")
        return

    # Save file information and ask for movie name
    await state.update_data(file_id=file_id, file_type=file_type)
    await message.reply("Please enter the name of the movie:")
    await UploadMovie.waiting_for_movie_name.set()

async def handle_movie_name(message: types.Message, state: FSMContext, movie_collection: Collection):
    movie_name = message.text.strip()
    user_data = await state.get_data()
    file_id = user_data.get("file_id")
    file_type = user_data.get("file_type")

    # Check for duplicates before saving
    if movie_collection.find_one({"name": movie_name, "file_id": file_id}):
        await message.reply("This file is already saved under that movie name.")
    else:
        movie_collection.insert_one({
            "name": movie_name,
            "file_id": file_id,
            "file_type": file_type,
            "uploaded_by": message.from_user.id
        })
        await message.reply(f"The movie '{movie_name}' has been successfully saved.")

    # Finish state
    await state.finish()

async def search_movie(message: types.Message, movie_collection: Collection):
    movie_name = message.text.strip()
    matching_movies = movie_collection.find({"name": {"$regex": f"^{movie_name}", "$options": "i"}})

    found = False
    for movie in matching_movies:
        found = True
        file_id = movie["file_id"]
        file_type = movie["file_type"]
        if file_type == "document":
            await message.answer_document(file_id)
        elif file_type == "video":
            await message.answer_video(file_id)

    if not found:
        await message.reply("Sorry, no movies found with that name.")

def register_handlers(dp: Dispatcher, movie_collection: Collection):
    dp.register_message_handler(handle_file_upload, content_types=[types.ContentType.DOCUMENT, types.ContentType.VIDEO], state="*", movie_collection=movie_collection)
    dp.register_message_handler(handle_movie_name, state=UploadMovie.waiting_for_movie_name, movie_collection=movie_collection)
    dp.register_message_handler(lambda message: message.text, lambda message: search_movie(message, movie_collection), content_types=types.ContentType.TEXT)
