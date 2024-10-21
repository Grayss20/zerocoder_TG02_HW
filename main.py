import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, OPENWEATHERMAP_API_KEY  # Store your OpenWeatherMap API key here
from aiogram.fsm.storage.memory import MemoryStorage
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

translator = Translator()  # Инициализация переводчика


@dp.message(Command("voice"))
async def voice(message: Message):
    voice = FSInputFile("Example.ogg")
    await bot.send_voice(message.chat.id, voice)


@dp.message(F.photo)
async def react_photo(message: Message):
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.answer("Ваше фото сохранено")


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply(f"Привет, {message.from_user.full_name}!")


@dp.message()
async def translate(message: Message):
    try:
        # Перевод текста на английский
        translated = translator.translate(message.text, dest='en')
        await message.answer(f"Перевод: {translated.text}")
    except Exception as e:
        await message.answer("Произошла ошибка при переводе текста")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
