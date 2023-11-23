from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from app.config import ADMIN_CHAT, ADMINS


router = Router(name=__name__)


@router.message(
    Command("start_dialog"),
    F.chat.type == 'private',
    F.from_user.id.in_(ADMINS)
)
async def start_dialog_handler(message: Message,command: CommandObject, bot: Bot):
    if not command.args:
        await message.answer(
            "Вкажіть аргументи!\n"
            "usage: `/start_dialog <chat_id>`",
            parse_mode='Markdown'
        )
        return

    chat_id = command.args.split(maxsplit=1)[0]

    try: 
        chat = await bot.get_chat(chat_id)
    except:
        await message.answer("Діалогу за вказаним ID не знайдено")
    else:
        if chat.type == 'private':
            name = f"{chat.first_name} {chat.last_name or ''}"
        else:
            name = chat.title

        await message.answer(
            f"id: {chat.id}\n"
            f"name: {name}\n\n"
            "Діалог розпочато!"
        )


@router.message(
    F.chat.type == 'private',
    F.reply_to_message.from_user.is_bot,
    F.reply_to_message.text.endswith('Діалог розпочато!'),
    F.from_user.id.in_(ADMINS)
)
async def send_msg_handler(message: Message, bot: Bot):
    await bot.send_message(
        chat_id=message.reply_to_message.text.split(maxsplit=2)[1],
        text=message.text,
        entities=message.entities,
        parse_mode=None
    )



from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey

def fix_storage_key(user_id,key: StorageKey) -> StorageKey:
    return StorageKey(
        user_id=user_id,
        chat_id=user_id,
        bot_id=key.bot_id,
        thread_id=key.thread_id,
        destiny=key.destiny,
    )

class AdminRequestState(StatesGroup):
    START = State()


@router.message(Command('request_admin'),F.chat.type == 'private')
async def command_help_handler(message: Message, bot:Bot, state: FSMContext):
    await state.set_state(AdminRequestState.START)

    user = message.from_user

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Закрити діалог",callback_data=f"close_admin_dialog={user.id}")],
        ]
    )

    await bot.send_message(ADMIN_CHAT,
            f"id: {user.id}\n"
            f"name: {user.full_name}\n\n"
            "Діалог розпочато!",
            reply_markup=keyboard
        )

    await message.answer("Діалог з адміном розпочто")


@router.callback_query(F.data.startswith("close_admin_dialog"))
async def send_random_value(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.data.split('=')[1]

    state.key = fix_storage_key(user_id,state.key)
    await state.clear()

    await callback.message.edit_text(callback.message.text,reply_markup=None)

    await bot.send_message(user_id,"Ваш діалог з адміністрацію завершено")


@router.message(AdminRequestState.START,F.chat.type == 'private')
async def forward_msg_handler(message: Message):
    await message.forward(ADMIN_CHAT)
