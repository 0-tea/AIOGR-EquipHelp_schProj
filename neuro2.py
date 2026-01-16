import openai

client = openai.OpenAI(
    api_key="",
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=""
)

response = client.responses.create(
    model="",
    input="Что я спросил тебя до этого ?",
    instructions = "Ты текстовый помощник который поддерживает пользователя и ведет теплый диалог",
)

print(response.output_text)
