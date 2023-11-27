from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest

from app.services.dialog import Dialog 

from app.config import ADMIN_CHAT


router = Router(name=__name__)


@router.message(Command('start_dialog'),F.chat.id==ADMIN_CHAT)
async def start_dialog_handler(message: Message,command: CommandObject, bot: Bot, state: FSMContext):
    if not command.args:
        await message.answer(
            "Вкажіть аргументи!\n"
            "usage: `/start_dialog <chat_id>`",
            parse_mode='Markdown'
        )
        return

    try: 
        dialog = await Dialog(
            session=state.storage.session,
            bot=bot,
            peer=command.args
        )
    except TelegramBadRequest:
        await message.answer("Діалогу за вказаним ID не знайдено")


@router.message(F.chat.type == 'private')
async def forward_msg_from_peer_handler(message: Message, bot: Bot, state: FSMContext):
    dialog = await Dialog(
        session=state.storage.session,
        bot=bot,
        peer=message.from_user.id,
        name=message.from_user.full_name
    )

    await message.copy_to(chat_id=dialog.admin_chat,message_thread_id=dialog.id)


@router.message(F.chat.id==ADMIN_CHAT,F.message_thread_id,~F.from_user.is_bot)
async def forward_msg_from_peer_handler(message: Message, bot: Bot, state: FSMContext):
    dialog = await Dialog(
        session=state.storage.session,
        bot=bot,
        id=message.message_thread_id,
    )
    if dialog:
        await message.copy_to(chat_id=dialog.peer)
