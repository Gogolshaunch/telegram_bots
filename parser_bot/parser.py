from aiogram.types import *
import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import datetime
from pytube import YouTube


load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv('Token'))


class FormState(StatesGroup):
    situation = State()

@dp.message(FormState.situation)
async def situation(msg: Message, state: FSMContext):
    url = msg.text
    yt = YouTube(url)
    await bot.send_message(msg.chat.id, f"*Начинаю загрузку видео* : *{yt.title}*\n"
                                        f'*С канала *: [{yt.author}]({yt.channel_url})', parse_mode='Markdown')
    await download(url, msg)


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
    await msg.answer("Введите ссылку на видео с YouTube, которое вы хотите загрузить: ")
    await state.set_state(FormState.situation)

async def download(url, msg):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4')
        stream.get_highest_resolution().download(f'{msg.chat.id}', f'{msg.chat.id}')
        with open(f'{msg.chat.id}/{msg.chat.id}', 'rb') as video:
            await bot.send_video(msg.chat.id, video, caption='Держи', parse_mode='Markdown')
            os.remove(f'{msg.chat.id}/{msg.chat.id}')
    except:
        await bot.send_message(msg.chat.id, "Ошибка! Видео слишком большое, я не могу его отправить")
        os.remove(f'{msg.chat.id}/{msg.chat.id}')


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
