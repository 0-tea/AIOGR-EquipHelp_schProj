from yandexcloud import SDK
import json
from dotenv import load_dotenv
import os

load_dotenv('tokens.env')
sdk = SDK(api_key=os.getenv('YANDEX_SERVICE_KEY'))

# Использование AI модели (пример для YandexGPT)
def ask_yandex_gpt(prompt, folder_id=os.getenv('YANDEX_FOLDER_KEY')):
    result = sdk.completions.create(
        model="general",  # или "general:rc", "summarization" и др.
        prompt=prompt,
        folder_id=folder_id,
        temperature=0.6,
        max_tokens=2000
    )
    return result.alternatives[0].text

# Пример вызова
response = ask_yandex_gpt("Привет! Как дела?")
print(response)