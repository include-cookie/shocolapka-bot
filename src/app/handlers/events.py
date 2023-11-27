from aiogram import Router, F
from aiogram.types import Message

from app.config import ADMIN_CHAT


router = Router(name=__name__)


@router.message(F.chat.type != 'private',~F.from_user.is_bot,F.chat.id!=ADMIN_CHAT)
async def events_handler(message: Message):
    pass
