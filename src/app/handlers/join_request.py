from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, ChatJoinRequest,
    ReplyKeyboardMarkup, ReplyKeyboardRemove,
    KeyboardButton
)

import random
from app.db.storage import fix_storage_key


router = Router(name=__name__)



class JoinRequestState(StatesGroup):
    START = State()
    RULES = State()
    BOT = State()
    HACKER = State()
    END = State()



@router.chat_join_request()
async def cjr_handler(request: ChatJoinRequest, state: FSMContext):
    state.key = fix_storage_key(state.key)

    await state.set_state(JoinRequestState.START)
    await state.set_data({"request_chat_id":request.chat.id})

    lst = [
        [KeyboardButton(text="Я Бот")],
        [KeyboardButton(text="Я Людина")],
        [KeyboardButton(text="0100101")],
    ]

    random.shuffle(lst)

    await request.answer_pm(
        f"Привіт, {request.from_user.full_name}!\n"
        'Я побачила що ти хочеш приєднатись до нашої спільноти "Програмісти і печеньки". '
        "Але перед тим як я тебе додам в групу, мушу переконатись що ти !bot",
        reply_markup=ReplyKeyboardMarkup(keyboard=lst)
    )



@router.message(JoinRequestState.START,F.text == 'Я Людина')
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
    await message.answer(
        "Хмм, ну добре повірю тобі поки.\n"
        "Я люблю цю місцину за те що у ній перебувають стільки чудових талановитих людей ❤️.\n"
        "Я піклюсь про кожного з них і хочу переконатись що ти будеш вести себе чемно :3\n\n"
        "<a href='https://telegra.ph/Use-pro-Program%D1%96sti-%D1%96-pechenki-08-21'>[Правила спільноти]</a>\n\n"
        "Обіцяєш вести себе чемно ?",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


@router.message(JoinRequestState.RULES,F.text == "Обіцяю")
async def rules_accept_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.END)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пропустити")],
        ]
    )

    await message.answer(
        "Чудово!\n\n"
        "І насамкінець, давай познайомимось!\n"
        "Представся, напиши про себе 2-3 речення.\n"
        "Xто ти? Чим займаєшся?\n"
        "Чим цікавишся? Що умієш? Що вивчаєш?\n"
        "Можливо маєш які плани на майбутнє?"
        ,reply_markup=keyboard
    )


@router.message(JoinRequestState.RULES,F.text == "Я Засранець")
async def rules_decline_handler(message: Message, state: FSMContext):
    await message.answer(
        "Ну ти і бака!\n"
        "Не пущу таких!"
    )



@router.message(JoinRequestState.END)
async def rules_decline_handler(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    request_chat_id = data.get('request_chat_id')
    await bot.approve_chat_join_request(request_chat_id,message.from_user.id)

    if message.text != 'Пропустити':
        await message.forward(chat_id=request_chat_id)

    await state.clear()
    await message.answer(
        f"Вітаю в чаті, {message.from_user.full_name}!",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Якщо у тебе будуть які запитання до адміністрації\n"
        "Не соромся пиши прямісінько сюди мені в чат\n"
        "Я все передам нашим адмінам :3"
    )



###############------    BOT    ------###############


@router.message(JoinRequestState.START,F.text == 'Я Бот')
async def bot_route_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.BOT)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Я Бот")],
            [KeyboardButton(text="Насправді я людина")],
        ]
    )

    await message.answer(
        "Ура ! Нарешті бот!\n"
        "А то мені постійно лише людиська пишуть.\n"
        "Давно я тут ботів не бачила.\n\n"
        "хоча ....\n"
        "а ти точно бот ? чи прикидаєшся ?",
        reply_markup=keyboard
    )


@router.message(JoinRequestState.BOT,F.text == "Я Бот")
async def bot_accept_handler(message: Message, state: FSMContext):
    await message.answer(
        "хммм ну добре ...\n"
        "як скажеш\n\n"
        "Еххх я б з тобою ще поспілкувалась. "
        "Aле наш адмін заборонив мені пускати в чат ботів.\n\n"
        "тому вибачай"
    )



###############------    HACKER    ------###############


@router.message(JoinRequestState.START,F.text == '0100101')
async def hacker_route_handler(message: Message, state: FSMContext):
    await state.set_state(JoinRequestState.HACKER)

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Насправді я людина")],
        ]
    )
    await message.answer("""
0JLRltGC0LDRjiEK0K/QutGJ0L4g0LLQuCDRhtC1INGH0LjRgtCw0ZTRgtC1LCDQvtGC0LbQtSDQ
stC4INGA0L7Qt9C/0L7Rh9Cw0LvQuCDQv9GA0L7RhdC+0LTQttC10L3QvdGPINC80ZbQvdGWIGhh
Y2tlciDQutCy0LXRgdGC0YMK0LTQu9GPINGC0LjRhSDRhdGC0L4g0LfQvdCw0ZQg0YLRgNC+0YjQ
utC4INCx0ZbQu9GM0YjQtSDQvdGW0LYg0LfQstC40YfQsNC50L3QuNC5INC60L7RgNC40YHRgtGD
0LLQsNGHCtC90LDQv9C40YjRltGC0Ywg0LIg0YfQsNGCICI0MiIg0YnQvtCxINC/0YDQvtC00L7Q
stC20LjRgtC4INGC0LAg0L7RgtGA0LjQvNCw0YLQuCDQvdCw0YHRgtGD0L/QvdC1INC30LDQstC0
0LDQvdC90Y8KCtGP0LrRidC+INCy0LDQvCDQvdCw0LTQvtGX0YHRgtGMINCw0LHQviDQsdGA0LDQ
utC90LUg0YHQuNC7LCDQstC4INC30LDQttC00Lgg0LzQvtC20LXRgtC1INC90LDRgtC40YHQvdGD
0YLQuCDQutC90L7Qv9C60YMKItC90LDRgdC/0YDQsNCy0LTRliDRjyDQu9GO0LTQuNC90LAiINGC
0LAg0L/RgNC+0LTQvtCy0LbQuNGC0Lgg0YHRgtCw0L3QtNCw0YDRgtC90YMg0L/RgNC+0YbQtdC0
0YPRgNGDINC00L7QtNCw0YfRliDQtNC+INGB0L/RltC70YzQvdC+0YLQuAo=
""" ,reply_markup=keyboard
    )


@router.message(JoinRequestState.HACKER,F.text)
async def hacker_accept_handler(message: Message, state: FSMContext):
    if  message.text == "42":
        await message.answer("Вітаю ви пройшли тест!",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Не та відповідь яку я хотіла отримати ...")
