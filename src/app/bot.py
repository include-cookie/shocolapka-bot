import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app import handlers 
from app.db.storage import SQLStorage

from app.config import TOKEN


async def main() -> None:
    bot = Bot(TOKEN,parse_mode=ParseMode.HTML)

    dp = Dispatcher(storage=SQLStorage())
    handlers.register(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
