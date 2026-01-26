from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


wait_router = Router()
chatForSup = -1003751729107

class supRespStat(StatesGroup):
    waitingForMissMessage = State()
    waitingForIdeaMessage = State()

@wait_router.message(supRespStat.waitingForMissMessage)
async def process_user_message(message: types.Message, state: FSMContext, bot: Bot):
    user = message.from_user

    await bot.send_message(
        chat_id=chatForSup,
        message_thread_id=None,
        text = f"💔 <strong>ОШИБКА В ИНСТРУКЦИЯХ</strong> \n \n"
                f"Пользователь @{user.username or message.from_user.id} обратился с <strong>ошибкой</strong> в инструкциях. \n"
               
                f"<blockquote expandable='true'>\n"
                f"{message.text}"
                f"</blockquote>",
        parse_mode="HTML"
    )

    await state.clear()
    await message.answer("Сообщение успешно переслано в чат поддержки")


@wait_router.message(supRespStat.waitingForIdeaMessage)
async def process_user_message(message: types.Message, state: FSMContext, bot: Bot):
    user = message.from_user

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
    await message.answer("Сообщение успешно переслано в чат поддержки")