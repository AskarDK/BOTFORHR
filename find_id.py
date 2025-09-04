import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

API_TOKEN = "8462945230:AAHEEklaV1hRtl8LzywvFvJcb_Gd2q7oeSM"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Подсказка при /start
@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    await msg.answer(
        "Привет! Я бот, который возвращает твой Telegram ID.\n"
        "Просто отправь мне /id"
    )

# Основной хендлер для /id
@dp.message(Command("id"))
async def cmd_id(msg: types.Message):
    await msg.answer(
        f"Ваш Telegram ID: <code>{msg.from_user.id}</code>",
        parse_mode="HTML"
    )
    logging.info(f"replied with ID {msg.from_user.id}")

if __name__ == "__main__":
    dp.run_polling(bot)
