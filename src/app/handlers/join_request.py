from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, ChatJoinRequest,
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
    KeyboardButton
)


router = Router(name=__name__)



class JoinRequestState(StatesGroup):
    START = State()
    RULES = State()
    BOT = State()
    HACKER = State()
    END = State()


# @router.chat_join_request()
# async def cjr_handler(request: ChatJoinRequest, state: FSMContext):
#     await state.update_data(request_chat_id=request.chat.id)
from aiogram.filters import Command


@router.message(Command("start_test"))
async def cjr_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.START)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Бот")],
            [KeyboardButton(text="Людина")],
            [KeyboardButton(text="0100101")],
        ]
    )

    await message.answer("Привіт!",reply_markup=keyboard)


@router.message(JoinRequestState.START,F.text == 'Людина')
@router.message(JoinRequestState.BOT,F.text == "Насправді я людина")
@router.message(JoinRequestState.HACKER,F.text == "Насправді я людина")
async def human_route_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.RULES)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Я Засранець")],
            [KeyboardButton(text="Обіцяю")],
        ]
    )
    await message.answer("Правила",reply_markup=keyboard)


@router.message(JoinRequestState.RULES,F.text == "Обіцяю")
async def rules_accept_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.END)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пропустити")],
        ]
    )

    await message.answer("Чудово",reply_markup=keyboard)


@router.message(JoinRequestState.RULES,F.text == "Я Засранець")
async def rules_decline_handler(message: Message, state: FSMContext):
    await message.answer("Бака")



@router.message(JoinRequestState.END)
async def rules_decline_handler(message: Message, state: FSMContext):
    #data = await state.get_data()

    #await bot.approve_chat_join_request(data.get('request_chat_id'),message.from_user.id)

    await state.clear()
    await message.answer(
        f"Вітаю в чаті, {message.from_user.full_name}!",
        reply_markup=ReplyKeyboardRemove()
    )



###############------    BOT    ------###############


@router.message(JoinRequestState.START,F.text == 'Бот')
async def bot_route_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.BOT)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Я Бот")],
            [KeyboardButton(text="Насправді я людина")],
        ]
    )
    await message.answer("БОТИ",reply_markup=keyboard)


@router.message(JoinRequestState.BOT,F.text == "Я Бот")
async def bot_accept_handler(message: Message, state: FSMContext):
    await message.answer("Бот бака")



###############------    HACKER    ------###############


@router.message(JoinRequestState.START,F.text == '0100101')
async def hacker_route_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.HACKER)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Насправді я людина")],
        ]
    )
    await message.answer("BASE64",reply_markup=keyboard)


@router.message(JoinRequestState.HACKER,F.text == "24")
async def hacker_accept_handler(message: Message, state: FSMContext):
    await message.answer("Hacker",reply_markup=ReplyKeyboardRemove())
