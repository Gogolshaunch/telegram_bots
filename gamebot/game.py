from aiogram.types import *
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command, state
from aiogram.fsm.context import FSMContext
from asyncio import sleep
import asyncio
import datetime
from aiogram.methods import send_dice

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv('Token'))


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

    await sleep(1)

    await msg.answer("Бросок бота")
    bot_data = await bot.send_dice(msg.chat.id, emoji='🎲')
    bot_data = bot_data.dice.value
    await sleep(5)

    await msg.answer("Ваш бросок")
    user_data = await bot.send_dice(msg.chat.id, emoji='🎲')
    user_data = user_data.dice.value
    await sleep(5)

    if bot_data > user_data:
        await msg.answer("Вы проиграли!")
    elif bot_data < user_data:
        await msg.answer("Вы победили!")
    else:
        await msg.answer("Ничья!")
    await msg.answer("/start")

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
