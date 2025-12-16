import openai

client = openai.OpenAI(
    api_key="AQVN1mZ0QJ85SWVmYADjEiUFDSGUFaSC-v_NMuZi",
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project="b1g9sc1evccct6821v5o"
)

response = client.responses.create(
    model="gpt://b1g9sc1evccct6821v5o/yandexgpt/rc",
    input="Что я спросил тебя до этого ?",
    instructions = "Ты текстовый помощник который поддерживает пользователя и ведет теплый диалог",
)

print(response.output_text)