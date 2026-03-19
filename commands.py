import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import neuroChatting
from inlineKeyBoard_db import kbBase_main_menu
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
import logging
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from neuroChatting import ChatStates, YandexNeuralChat

router = Router()
logger = logging.getLogger(__name__)


class LoggingCommandMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if event.text and event.text.startswith('/'):
            user_name = event.from_user.username or "emptyUS"
            command = event.text.split()[0]
            logger.info(f"[COMMAND] User: [{user_name}] | Command: [{command}]")
        return await handler(event, data)

router.message.middleware(LoggingCommandMiddleware())


'''@router.message(F.photo)
async def start_command(message: Message):
    photo = message.photo[-1]
    await message.answer(f"{photo}")'''


@router.message(Command("getid"))
async def get_chat_id(message: types.Message):
    chat_info = (
        f"👤 Ваш ID: `{message.from_user.id}`\n"
        f"💬 ID этого чата: `{message.chat.id}`\n"
        f"📝 Тип чата: {message.chat.type}\n"
        f"{message.message_thread_id}\n"
    )

    if message.chat.type in ["group", "supergroup"]:
        chat_info += f"📛 Название группы: {message.chat.title}"

    await message.answer(chat_info, parse_mode="Markdown")

@router.message(CommandStart())
async def start_cmd_about(message: types.Message):
    text = ("Это бот нацелен на помощь и поддержку как школьников, так и учителей и преподователей"
            " для этого отправьте команду /main")
    pictireFile = open('resources/start_picture').read().strip()
    await message.answer_photo(photo=pictireFile, caption=text)


@router.message(Command("main"))
async def start_command(message: Message, state: FSMContext):
    if await state.get_state() == ChatStates.IsNeuralChatting:
        await state.clear()
        await message.answer("Вы вышли из режима общения с ИИ")
        YandexNeuralChat.clear_chat(YandexNeuralChat(), user_id=message.from_user.username or message.from_user.id)
        await asyncio.sleep(0.6)

    logger.info(f"[COMMAND] [{message.from_user.username}] отправил команду [/main]")
    pictireFile = open('resources/mein_picture').read().strip()
    text = ("Добро пожаловать! Выберите опцию: "
            "\n    🖨 - хранилище инструкций "
            "\n    🎨 - Открывает диалог с нейронной сетью"
            "\n    🎮 - Комнаты для обучения"
            "\n    ⛑ - Связь с разработчиками, предложка идей")
    await message.answer_photo(
        photo=pictireFile,
        caption=text,
        reply_markup=kbBase_main_menu.main_menu_view()
    )