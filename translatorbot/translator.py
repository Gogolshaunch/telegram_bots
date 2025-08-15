import json

from aiogram.types import *
import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import datetime
import random
from googletrans import Translator
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv('Token'))
translator = Translator()
LIST_FILE = "lists.json"

def load_data(file):
    with open(file, 'r') as f:
        try:
            data = json.load(f)
        except:
            return {}
    return data

def save_data(file, data):
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)

class FormState(StatesGroup):
    situation = State()


@dp.message(FormState.situation)
async def situation(msg: Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    text = msg.text.strip()
    text_list = load_data(LIST_FILE)
    text_list[user_id] = text
    save_data(LIST_FILE, text_list)
    await state.clear()

    keyboard_builder1 = InlineKeyboardBuilder()
    keyboard_builder1.add(InlineKeyboardButton(text="Английский", callback_data="en"))
    keyboard_builder1.add(InlineKeyboardButton(text="Испанский", callback_data="ispan"))
    keyboard_builder1.add(InlineKeyboardButton(text="Немецкий", callback_data="nem"))
    keyboard_builder1.add(InlineKeyboardButton(text="Французский", callback_data="franc"))
    keyboard_builder1.add(InlineKeyboardButton(text="Итальянский", callback_data="italic"))
    keyboard_builder1.add(InlineKeyboardButton(text="Корейский", callback_data="cor"))
    keyboard_builder1.add(InlineKeyboardButton(text="Португальский", callback_data="port"))
    keyboard_builder1.add(InlineKeyboardButton(text="Арабский", callback_data="arb"))
    keyboard_builder1.add(InlineKeyboardButton(text="Китайский", callback_data="chine"))
    keyboard_builder1.add(InlineKeyboardButton(text="Японский", callback_data="jap"))
    await msg.answer("Выберите язык",reply_markup=keyboard_builder1.as_markup(), )


@dp.callback_query(lambda c: c.data in ["en", "ispan", "nem", "franc", "italic", "cor", "port", "arb", "chine", "jap"])
async def process_status_selection(callback: CallbackQuery, state: FSMContext):
    user_id = str(callback.from_user.id)
    text_list = load_data(LIST_FILE)
    text1 = text_list[user_id]
    if callback.data == "en":
        result = translator.translate(text1, src='ru', dest='en')
    elif callback.data == "ispan":
        result = translator.translate(text1, src='ru', dest='es')
    elif callback.data == "nem":
        result = translator.translate(text1, src='ru', dest='de')
    elif callback.data == "franc":
        result = translator.translate(text1, src='ru', dest='fr')
    elif callback.data == "italic":
        result = translator.translate(text1, src='ru', dest='it')
    elif callback.data == "cor":
        result = translator.translate(text1, src='ru', dest='ko')
    elif callback.data == "port":
        result = translator.translate(text1, src='ru', dest='pt')
    elif callback.data == "arb":
        result = translator.translate(text1, src='ru', dest='ar')
    elif callback.data == "chine":
        result = translator.translate(text1, src='ru', dest='zh-tw')
    elif callback.data == "jap":
        result = translator.translate(text1, src='ru', dest='ja')
    await callback.message.answer(result.text)
    await callback.answer()

@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext):
    now = datetime.datetime.now()
    if 6 <= now.hour < 12:
        await msg.answer("Доброе утро!")
    elif 12 <= now.hour < 18:
        await msg.answer( "Добрый день!")
    elif 18 <= now.hour < 23:
        await msg.answer( "Добрый вечер!")
    else:
        await msg.answer("Доброй ночи!")
    await msg.answer("Введите текст:")
    await state.set_state(FormState.situation)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
