from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
'''
54 - ошибки
40 - предложка 
'''

wait_router = Router()
chatForSup = -1003751729107

def checkAttach(message: types.Message) -> bool:
    media_types = [
        'photo', 'video', 'document', 'animation',
        'voice', 'video_note', 'sticker', 'audio'
    ]
    return message.content_type in media_types

class supRespStat(StatesGroup):
    waitingForMissMessage = State()
    waitingForIdeaMessage = State()

@wait_router.message(supRespStat.waitingForMissMessage)
async def process_user_message(message: types.Message, state: FSMContext, bot: Bot):
    '''ОШИБКА СОО'''
    user = message.from_user
    if checkAttach(message):
        await bot.send_message(
            chat_id=chatForSup,
            message_thread_id=54,
            text=f"💔 <strong>ОШИБКА В ИНСТРУКЦИЯХ</strong> \n \n"
                 f"Пользователь @{user.username or message.from_user.id} обратился с <strong>ошибкой</strong> в инструкциях. \n",
            parse_mode="HTML"
        )

        await bot.forward_message(
            chat_id=chatForSup,
            message_thread_id=54,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
    else:
        await bot.send_message(
            chat_id=chatForSup,
            message_thread_id=54,
            text = f"💔 <strong>ОШИБКА В ИНСТРУКЦИЯХ</strong> \n \n"
                    f"Пользователь @{user.username or message.from_user.id} обратился с <strong>ошибкой</strong> в инструкциях. \n"
                   
                    f"<blockquote expandable='true'>\n"
                    f"{message.text}"
                    f"</blockquote>",
            parse_mode="HTML"
        )

    await state.clear()
    await message.answer("Сообщение успешно переслано в чат поддержки, благодарим за бдительность!")


@wait_router.message(supRespStat.waitingForIdeaMessage)
async def process_user_message(message: types.Message, state: FSMContext, bot: Bot):
    '''ПРЕДЛОЖКА СОО'''
    user = message.from_user
    if checkAttach(message):
        await bot.send_message(
            chat_id=chatForSup,
            message_thread_id=40,
            text=f"💚 <strong>Предложка</strong> \n \n"
                    f"Пользователь @{user.username or message.from_user.id} обратился с <strong>предложением</strong> в инструкциях. \n",
            parse_mode="HTML")

        await bot.forward_message(
            chat_id=chatForSup,
            message_thread_id=40,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
    else:
        await bot.send_message(
            chat_id=chatForSup,
            message_thread_id=40,
            text=f"💚 <strong>Предложка</strong> \n \n"
                 f"Пользователь @{user.username or message.from_user.id} обратился с <strong>предложением</strong> в инструкциях. \n"
    
                 f"<blockquote expandable='true'>\n"
                 f"{message.text}"
                 f"</blockquote>",
            parse_mode="HTML"
        )

    await state.clear()
    await message.answer("Сообщение успешно переслано в чат поддержки. Благодарим за помощь в улучшении проекта!")