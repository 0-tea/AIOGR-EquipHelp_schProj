import logging
from typing import Dict, List

import requests
import json
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
import os

load_dotenv('tokens.env')
logger = logging.getLogger(__name__)
wait_router = Router()
class ChatStates(StatesGroup):
    IsNeuralChatting = State()

class YandexNeuralChat:
    def __init__(self):
        self.key = os.getenv('YANDEX_SERVICE_KEY')
        self.folder = os.getenv('YANDEX_FOLDER_KEY')
        self.memory: Dict[int, List[dict]] = {}
        '''История чата user_id - [messages]'''

    def stop_word(self, text):
        return text.lower() in ['стоп', 'stop', 'выход']

    def clear_chat(self, user_id, state: FSMContext):
        state.clear()
        if user_id in self.memory:
            del self.memory[user_id]

    @wait_router.message(ChatStates.IsNeuralChatting)
    async def response(self, user_id, text):
        # Инициализация истории
        if user_id not in self.memory:
            self.memory[user_id] = []

        # Добавляем вопрос
        self.memory[user_id].append({"role": "user", "text": text})

        # API запрос
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {"Authorization": f"Api-Key {self.key}"}

        data = {
            "modelUri": f"gpt://{self.folder}/yandexgpt",
            "messages": self.memory[user_id][-6:],  # Последние 3 пары
            "completionOptions": {"temperature": 0.6}
        }

        r = requests.post(url, headers=headers, json=data)
        answer = r.json()["result"]["alternatives"][0]["message"]["text"]

        # Сохраняем ответ
        self.memory[user_id].append({"role": "assistant", "text": answer})
        print(answer)
        return answer

    def fdsf(self):
        print(self.response(123, "Привет!"))






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
