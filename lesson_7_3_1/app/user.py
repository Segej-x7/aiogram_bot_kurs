from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import Chat
from app.generators import gpt_text
from app.database.requests import set_user

user = Router()


# Обработчик для команды /start
@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Добро пожаловать!', reply_markup=kb.main)


# Обработчик для текста "Чат"
@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer('Введите ваш запрос')


# Обработчик для состояния Chat.text
@user.message(Chat.text)
async def chet_response(message: Message, state: FSMContext):
    await state.set_state(Chat.wait)
    response = await gpt_text(message.text, 'gpt-4o-mini')
    await message.answer(response)
    await state.clear()


@user.message(Chat.wait)
async def wait_wait(message: Message):
    await message.answer('Ваше сообщение генерируется, подождите.')
