from operator import attrgetter
import uuid
from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from app.config import ADMIN_CHAT, MAIN_SITE_URL, PANDC_CHAT_ID, DEBUG
from app.services.token_gen import gen_token
# from app.utils.helpers import IsAdmin

from aiogram.utils.deep_linking import decode_payload
from aiogram.types import Message, ChatMemberAdministrator, ChatMemberRestricted, ChatMemberOwner, ChatMemberMember

router = Router(name=__name__)


@router.message(CommandStart(deep_link=True),F.chat.type == 'private')
async def command_start_handler(message: Message, command: CommandObject, bot: Bot):
    args = command.args
    if(args == None): await message.answer(f"Привіт, {message.from_user.full_name}!")
    if(args == "signin"): await sign_in_message(message, bot)
    

@router.message(Command('help'),F.chat.id==ADMIN_CHAT)
async def command_admin_help_handler(message: Message):
    await message.answer(
        "Довідка:\n\n"
        "- /start_dialog - розпочати діалог від імені бота\n"
        "\nКоманди які використовуються виключно в групі:\n"
        "- /mute - замютити користувача\n"
        "- /warn - видати попередження\n"
        "- /rule - правила\n"
    )


@router.message(Command('help'),F.chat.type == 'private')
async def command_help_handler(message: Message):
    await message.answer(
        "Чим я можу допомогти ?\n\n"
        "Напишіть в чат щоб почати діалог з адміністрацією"
    )


@router.message(Command('signin'),F.chat.type == 'private')
async def command_help_handler(message: Message, bot: Bot):
    chatId = PANDC_CHAT_ID
    userId = message.from_user.id

    try:
        isUserMember = await IsChatMember(chatId, userId, bot)
        if(isUserMember): await sign_in_message(message, bot)
        else: await message.answer(
            "Печеньки тільки для учасників чату 👀"
        )
    except: await message.answer(
        "Помилка серверу"
    )
    

async def sign_in_message(message: Message, bot: Bot):
    user = message.from_user

    roles = ['user']
    photo_src=""
    profile_photos = await user.get_profile_photos()
    if(profile_photos.total_count > 0):
        photo_sizes = profile_photos.photos[0]
        big_photo_id = max(photo_sizes, key=attrgetter('file_size')).file_id
        file = await bot.get_file(big_photo_id)
        photo_src = file.file_path
    
    # if(await IsAdmin(message)): roles.append("admin")

    new_token = await gen_token(str(uuid.uuid1()), user.id, user.username, roles, photo_src, user.full_name)
    signin_url = f"{MAIN_SITE_URL}/signin/token?token={new_token}"

    main_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = "Sign in", url=signin_url), ]
    ],)

    await message.answer(
        "Хей-хей! Твій свіжоспечений токен уже готовий 🍪 мяя~\n\n"
        f"<pre language='json'>{new_token}</pre>\n\n"
        "Скопіюй його у форму на сайті :3\n\n"
        "Або тицни кнопочку нижче, щоб увійти миттєво на цьому пристрої\n\n",
        reply_markup=main_kb
    )

async def IsChatMember(chat_id: str, user_id: str, bot: Bot) -> bool:
    if(DEBUG): return True # ONLY DEV MODE!!!
    if(user_id == ""): return False

    member = await bot.get_chat_member(chat_id, user_id)
    if isinstance(member, ChatMemberOwner):
        return True
    elif isinstance(member, ChatMemberAdministrator):
        return True
    elif isinstance(member, ChatMemberRestricted):
        return True
    elif isinstance(member, ChatMemberMember):
        return True
    else:
        return False