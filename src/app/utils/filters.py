from aiogram.filters import Filter
from aiogram.types import Message


class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        admins = await message.chat.get_administrators()
        admins_ids = {admin.user.id for admin in admins}
        return (message.from_user.id in admins_ids)
