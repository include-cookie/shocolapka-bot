from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Filter, Command, CommandObject
from datetime import timedelta

from app.services.restrictions import give_warn, give_mute
from app.utils.timedelta import parse_delta

from app.utils.filters import IsAdmin


router = Router(name=__name__)


@router.message(
    Command("warn"),
    F.reply_to_message.from_user,
    IsAdmin()
)
async def command_warn_handler(message: Message,state: FSMContext):
    user = message.reply_to_message.from_user

    cnt = await give_warn(
        state.storage.session,
        message.chat.id,
        user.id
    )

    await message.answer(
        f'Попередження для <a href="tg://user?id={user.id}">{user.full_name}</a>'
        + (f'\nЦе уже {cnt} попередження!' if cnt > 2 else '')
    )


@router.message(
    Command("mute"),
    F.reply_to_message.from_user,
    IsAdmin()
)
async def command_mute_handler(message: Message,command: CommandObject, bot: Bot):
    user = message.reply_to_message.from_user

    if command.args:
        period = parse_delta(command.args)
        period = period if period else timedelta(minutes=5)
    else:
        period = timedelta(minutes=5)

    await give_mute(bot,message.chat.id,user.id,period)

    await message.answer(
        f'Замютчено, <a href="tg://user?id={user.id}">{user.full_name}</a>'
    )


@router.message(
    Command("mute"),
    ~IsAdmin()
)
async def command_automute_handler(message: Message, bot: Bot):
    user = message.from_user

    await give_mute(bot,message.chat.id,user.id,timedelta(minutes=2))

    await message.answer(
        'Отакої!\n'
        f'<a href="tg://user?id={user.id}">{user.full_name}</a> вирішив самозамютитись ...'
    )
