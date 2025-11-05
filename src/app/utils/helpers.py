import asyncio
from aiogram.types import Message

async def IsAdmin(message: Message) -> bool:
    admins = await message.chat.get_administrators()
    admins_ids = {admin.user.id for admin in admins}
    return (message.from_user.id in admins_ids)