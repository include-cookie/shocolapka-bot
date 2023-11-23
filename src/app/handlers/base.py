from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from app.config import ADMINS


router = Router(name=__name__)


@router.message(CommandStart(),F.chat.type == 'private')
async def command_start_handler(message: Message,state: FSMContext):
    current_state = await state.get_state()
    await message.answer(f"Привіт, {message.from_user.full_name}!")


@router.message(
    Command('help'),
    F.chat.type == 'private',
    F.from_user.id.in_(ADMINS)
)
async def command_admin_help_handler(message: Message):
    await message.answer(
        "Довідка:\n\n"
        "- /start_dialog - розпочати діалог від імені бота\n"
        "\nКоманди які використовуються виключно в групі:\n"
        "- /mute - замютити користувача\n"
        "- /warn - видати попередження"
    )


@router.message(Command('help'),F.chat.type == 'private')
async def command_help_handler(message: Message):
    await message.answer(
        "Чим я можу допомогти ?\n\n"
        "/request_admin - почати діалог з адміністрацією"
    )


@router.message(F.chat.type == 'private')
async def comman_msg_handler(message: Message):
    await message.answer(
        "Вибачте не зрозуміла вашої команди ((\n\n"+
        ("/request_admin - почати діалог з адміністрацією"
        if message.from_user.id not in ADMINS else '')
    )
