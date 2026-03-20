import asyncio
import logging
from typing import Dict, List
from aiogram import types
import requests
from aiogram import Router
from inlineKeyBoard_db import kbBase_main_menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
import os



load_dotenv('tokens.env')
logger = logging.getLogger(__name__)
wait_router_Ai = Router()
class ChatStates(StatesGroup):
    IsNeuralChatting = State()

class YandexNeuralChat:

    def __init__(self):
        self.key = os.getenv('YANDEX_SERVICE_KEY')
        self.folder = os.getenv('YANDEX_FOLDER_KEY')
        self.memory: Dict[str, List[dict]] = {}
        '''История чата user_id - [messages]'''

    @staticmethod
    def clear_chat(self, user_id):
        if user_id in self.memory:
            del self.memory[user_id]

    @staticmethod
    async def response(self, user_id, text):
        # История
        if user_id not in self.memory:
            self.memory[user_id] = []

        # Адд в историю
        self.memory[user_id].append({"role": "user", "text": text})

        # API запрос
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {"Authorization": f"Api-Key {self.key}"}

        data = {
            "modelUri": f"gpt://{self.folder}/yandexgpt",
            "messages": self.memory[user_id][-6:],  # Последние 3 пары
            "completionOptions": {"temperature": 0.3}
        }

        r = requests.post(url, headers=headers, json=data)
        answer = r.json()["result"]["alternatives"][0]["message"]["text"]

        # Сохранение ответа в дб
        self.memory[user_id].append({"role": "assistant", "text": answer})

        logger.info(answer)
        return answer
@wait_router_Ai.message(ChatStates.IsNeuralChatting)
async def ai_resp(message: types.Message, state: FSMContext):
    print(ChatStates.IsNeuralChatting)
    if message.text.lower() in ['стоп', 'stop', 'выход', '/main'] or message.text=='/main':

        YandexNeuralChat.clear_chat(YandexNeuralChat(), user_id=message.from_user.username or message.from_user.id)
        await state.clear()
        await message.answer("Вы вышли из режима общения с ИИ")

        await asyncio.sleep(0.6)
        pictireFile = open('resources/mein_picture').read().strip()
        text = ("Выберите опцию из предложенных ниже: "
                "\n    🖨 - хранилище инструкций "
                "\n    🎨 - Открывает диалог с нейронной сетью"
                "\n    🎮 - Комнаты для обучения"
                "\n    ⛑ - Связь с разработчиками, предложка идей")
        await message.answer_photo(
            photo=pictireFile,
            text=text,
            reply_markup=kbBase_main_menu.main_menu_view()
        )
    else:
        respAi = await YandexNeuralChat.response(YandexNeuralChat(), user_id=message.from_user.username or message.from_user.id, text=message.text)
        await message.answer(respAi)






'''def debug_request(prompt):
    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers={
            "Authorization": f"Bearer {token}",
            "x-folder-id": folder,
            "Content-Type": "application/json"
        },
        json={
            "modelUri": f"gpt://{folder}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 20000
            },
            "messages": [
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }
    )

    print("Статус:", response.status_code)
    print("Ответ полностью:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    return response

# Запусти это
debug_request("Привет")'''
