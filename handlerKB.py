from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
import logging
from aiogram.dispatcher.middlewares.base import BaseMiddleware

router = Router()
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: CallbackQuery, data: dict):
        user_name = event.from_user.username or "emptyUS"
        callback_data = event.data
        logger.info(f"[CALLBACK] User: [{user_name}] | Data: [{callback_data}]")
        return await handler(event, data)

router.callback_query.middleware(LoggingMiddleware())


@router.callback_query(F.data == "equip")
async def handle_equip(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали: Оборудование")
    await callback_query.answer()

@router.callback_query(F.data == "neuro")
async def handle_neuro(callback_query: CallbackQuery):
    await callback_query.message.edit_caption(
        caption="Запускается режим общения с нейронной сетью, напишите стоп, что бы из него выйти"
    )
    await callback_query.answer()

@router.callback_query(F.data == "room")
async def handle_room(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали: Комнаты")
    await callback_query.answer()

@router.callback_query(F.data == "support")
async def handle_support(callback_query: CallbackQuery):
    await callback_query.message.answer("Вы выбрали: Поддержка")
    await callback_query.answer()
