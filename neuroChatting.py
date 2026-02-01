
from dotenv import load_dotenv
import os
load_dotenv('tokens.env')

import requests
import json

TOKEN = os.getenv('YANDEX_SERVICE_KEY')
FOLDER = os.getenv('YANDEX_FOLDER_KEY')

def debug_request(prompt):
    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "x-folder-id": FOLDER,
            "Content-Type": "application/json"
        },
        json={
            "modelUri": f"gpt://{FOLDER}/yandexgpt-lite",
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
debug_request("Привет")
