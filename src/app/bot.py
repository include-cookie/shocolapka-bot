import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from app import handlers
from app.db import AsyncScopedSession
from app.db.storage import SQLStorage

from app.config import TOKEN


async def release_db_session_middleware(handler, event, data):
    try:
        return await handler(event, data)
    finally:
        await AsyncScopedSession.remove()


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        )
    )

    dp = Dispatcher(storage=SQLStorage())
    dp.update.outer_middleware(release_db_session_middleware)
    handlers.register(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
