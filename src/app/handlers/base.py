from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from app.config import ADMIN_CHAT


router = Router(name=__name__)


@router.message(CommandStart(),F.chat.type == 'private')
async def command_start_handler(message: Message,state: FSMContext):
    current_state = await state.get_state()
    await message.answer(f"Привіт, {message.from_user.full_name}!")


@router.message(Command('help'),F.chat.id==ADMIN_CHAT)
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
        "Напишіть в чат щоб почати діалог з адміністрацією"
    )
