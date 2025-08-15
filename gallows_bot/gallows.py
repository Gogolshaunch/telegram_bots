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

HANGMAN = (
            """
             ------
             |    |
             |
             |
             |
             |
             |
            ----------
            """,
            """
             ------
             |    |
             |    O
             |
             |
             |
             |
            ----------
            """,
            """
             ------
             |    |
             |    O
             |    |
             | 
             |   
             |    
            ----------
            """,
            """
             ------
             |    |
             |    O
             |   /|
             |   
             |   
             |   
            ----------
            """,
            """
             ------
             |    |
             |    O
             |   /|\\
             |   
             |   
             |     
            ----------
            """,
            """
             ------
             |    |
             |    O
             |   /|\\
             |   /
             |   
             |    
            ----------
            """,
            """
             ------
             |    |
             |    O
             |   /|\\
             |   / \\
             |   
             |   
            ----------
            """)

max_wrong = len(HANGMAN) - 1
WORDS = ('воздействие', 'телевизор', 'профессия', 'специалист', 'соответствие', 'обращение', 'покупатель', 'понимание', 'направление', 'формирование', 'государство', 'администрация' 'территория', 'президент', 'воспоминание', 'выступление', 'абитуриент', 'абсолютизм',
        'абстракция', 'авантюрист', 'авиалайнер', 'австралиец', 'автогигант', 'автотрасса', 'руководитель', 'законодательство', 'основание', 'лейтенант', 'перспектива', 'поверхность', 'получение', 'начальник', 'подразделение', 'возможность',
        'впрягание', 'горючесть', 'беженство', 'разведение', 'адсорбент', 'ослабевание', 'суверенитет', 'репатриантка', 'неудобство',)

word = random.choice(WORDS)
so_far = "_" * len(word)
wrong = 0
used = []

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv('Token'))

class FormState(StatesGroup):
    situation = State()


@dp.message(FormState.situation)
async def situation(msg: Message, state: FSMContext):
    text = msg.text.lower()
    global wrong, so_far, word
    guess = text
    if guess in used:
        await bot.send_message(msg.chat.id, f"Вы уже вводили букву {guess}")
        await bot.send_message(msg.chat.id, "\nВведите свое предположение: ")
    used.append(guess)
    if guess in word:
        await bot.send_message(msg.chat.id, f"\nДа! {guess} есть в слове!")
        new = ""
        for i in range(len(word)):
            if guess == word[i]:
                new += guess
            else:
                new += so_far[i]
        so_far = new
    else:
        await bot.send_message(msg.chat.id, f"\nИзвините, буквы {guess} нет в слове.")
        wrong += 1
    if wrong == max_wrong:
        await bot.send_message(msg.chat.id,HANGMAN[wrong])
        await bot.send_message(msg.chat.id,"\nТебя повесили!")
        await bot.send_message(msg.chat.id, f"\nЗагаданное слово было {word}")
        await state.clear()
        await bot.send_message(msg.chat.id, '/start')
    elif word == so_far:
        await bot.send_message(msg.chat.id,"\nВы угадали слово!")
        await bot.send_message(msg.chat.id, f"\nЗагаданное слово было {word}")
        await state.clear()
        await bot.send_message(msg.chat.id, '/start')
    else:
        await bot.send_message(msg.chat.id, HANGMAN[wrong])
        await bot.send_message(msg.chat.id, f'\nВы использовали следующие буквы: {used}\n')
        await bot.send_message(msg.chat.id, f'\nНа данный момент слово выглядит так: {so_far}\n')
        await bot.send_message(msg.chat.id, "\nВведите свое предположение: ")


@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext):
    global wrong, so_far, word
    now = datetime.datetime.now()
    if 6 <= now.hour < 12:
        await msg.answer("Доброе утро!")
    elif 12 <= now.hour < 18:
        await msg.answer( "Добрый день!")
    elif 18 <= now.hour < 23:
        await msg.answer( "Добрый вечер!")
    else:
        await msg.answer("Доброй ночи!")

    await msg.answer(f"Давай сыграем в игру виселица. Правила просты. Угадай загаданное слово по буквам пока тебя не повесели")
    await bot.send_message(msg.chat.id, HANGMAN[wrong])
    await bot.send_message(msg.chat.id, f'\nВы использовали следующие буквы: {used}\n')
    await bot.send_message(msg.chat.id, f'\nНа данный момент слово выглядит так: {so_far}\n')
    await bot.send_message(msg.chat.id, "\nВведите свое предположение: ")
    await state.set_state(FormState.situation)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
