import openai

async def neuro(message):
    client = openai.OpenAI(
        api_key="",
        base_url="https://rest-assistant.api.cloud.yandex.net/v1",
        project=""
    )

    response = client.responses.create(
        model="",
        input=f"{message.id}",
        instructions = "Ты текстовый помощник который поддерживает пользователя и ведет теплый диалог",
    )

    return response.output_text
