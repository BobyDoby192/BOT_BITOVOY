from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
import asyncio
import logging
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from handlers import catalog

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(catalog.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
