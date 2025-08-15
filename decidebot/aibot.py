from aiogram.types import *
import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command, state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BotCommand
import requests
import json

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv('Token'))

class FormState(StatesGroup):
    situation = State()
    option = State()

MODEL = "deepseek/deepseek-r1"
P_FILE = "person.json"

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

def load_prompt(user_id):
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()
    list_t = load_data(P_FILE)
    prompt += f'Теперь разберите на основе этой инструкции данную ситуацию: {list_t[user_id][0]}, Варианты: {list_t[user_id][1:]}'
    return prompt

def load_text(resp):
    with open('text.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()
    prompt += f'Текст нейросети: {resp}'
    return prompt

def process_content(content):
    return content.replace('<think>', '').replace('</think>', '')

async def set_commands():
    commands = [
        BotCommand(command="/info", description="Получить информацию обо мне"),
        BotCommand(command="/question", description="Задать вопрос")
    ]
    await bot.set_my_commands(commands)

@dp.message(FormState.situation)
async def situation(msg: Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    task_e = msg.text.strip()
    list_task = load_data(P_FILE)
    await state.clear()
    list_task[user_id].append(task_e)
    save_data(P_FILE, list_task)
    await msg.answer("Я понял. Теперь отправь первый вариант выбора")
    await state.set_state(FormState.option)

@dp.message(FormState.option)
async def option(msg: Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    task_e = msg.text.strip()
    list_task = load_data(P_FILE)

    if task_e.lower() == "стоп":
        await msg.answer("Я всё понял, подождите немного")
        await state.clear()
        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('API_KEY')}",
                "Content-Type": "application/json"
            }

            data = {
                "model": MODEL,
                "messages": [{"role": "user", "content": load_prompt(user_id)}],
                "stream": True
            }

            with requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    stream=True
            ) as response:
                full_response = []
                for chunk in response.iter_lines():
                    if chunk:
                        chunk_str = chunk.decode('utf-8').replace('data: ', '')
                        try:
                            chunk_json = json.loads(chunk_str)
                            if "choices" in chunk_json:
                                content = chunk_json["choices"][0]["delta"].get("content", "")
                                if content:
                                    cleaned = process_content(content)
                                    full_response.append(cleaned)
                        except:
                            pass

            print(''.join(full_response))

            text_data = {
                "model": MODEL,
                "messages": [{"role": "user", "content": load_text(''.join(full_response))}],
                "stream": True
            }
            with requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=text_data,
                    stream=True
            ) as answer_resp:
                answer_resp_full = []
                for chunk in answer_resp.iter_lines():
                    if chunk:
                        chunk_str = chunk.decode('utf-8').replace('data: ', '')
                        try:
                            chunk_json = json.loads(chunk_str)
                            if "choices" in chunk_json:
                                content = chunk_json["choices"][0]["delta"].get("content", "")
                                if content:
                                    cleaned = process_content(content)
                                    answer_resp_full.append(cleaned)
                        except:
                            pass
                await msg.answer(''.join(answer_resp_full), end='', flush=True)

            list_task[user_id].clear()
            save_data(P_FILE, list_task)
        except:
            await msg.answer("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже")
    else:
        list_task[user_id].append(task_e)
        save_data(P_FILE, list_task)
        await msg.answer("Вариант принят. Присылай ещё или напиши 'стоп'")

@dp.message(CommandStart())
async def command_start_handler(msg: Message):
    await msg.answer('Привет! Ты стоишь перед сложным выбором? Запускай /question и я тебе помогу')

@dp.message(Command("question"))
async def question(msg: Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    list_task = load_data(P_FILE)
    list_task[user_id] = []
    save_data(P_FILE, list_task)
    await msg.answer('Опиши ситуацию, в которой ты оказался, со всеми обстоятельствами как можно подробнее')
    await state.set_state(FormState.situation)

@dp.message(Command("info"))
async def info(msg: Message):
    await msg.answer('Я бот для помощи в принятии решений, опиши мне ситуацию, отправь варианты выбора и я оценю их с точки зрения выгоды, закона, морали и выберу объективно лучший вариант. НО не забывай, что ты сам должен подумать и решить все для себя')

async def main() -> None:
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
