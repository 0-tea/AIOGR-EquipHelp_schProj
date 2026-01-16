from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from inlineKeyBoard_db import kb_sup_view, kb_main_view, kb_test
import logging
from aiogram.dispatcher.middlewares.base import BaseMiddleware
import asyncio

router = Router()
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: CallbackQuery, data: dict):
        user_name = event.from_user.username or "emptyUS"
        callback_data = event.data
        logger.info(f"[CALLBACK] User: [{user_name}] | Data: [{callback_data}]")
        return await handler(event, data)

router.callback_query.middleware(LoggingMiddleware())


class test:
    def __init__(self):
        router.callback_query(F.data == "1")(self.handle_1)
        router.callback_query(F.data == "2")(self.handle_2)
        router.callback_query(F.data == "3")(self.handle_3)
        router.callback_query(F.data == "4")(self.handle_4)

    async def handle_1(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Просто отправляется новое",
                                            reply_markup=kb_test())
        await callback_query.answer()

    async def handle_2(self, callback_query: CallbackQuery):
        await callback_query.message.edit_text(
            text="Редактирует сообщение",  reply_markup=kb_test()
        )
        await callback_query.answer()


    async def handle_3(self, callback_query: CallbackQuery):
        await callback_query.message.delete()
        await asyncio.sleep(1)
        await callback_query.message.answer("Удаляет, ждет 1 секунду, отправляет",
                                            reply_markup=kb_test())
        await callback_query.answer()

    async def handle_4(self, callback_query: CallbackQuery):
        message = await callback_query.message.answer("loading... 123321")
        await asyncio.sleep(0.5)
        await message.delete() ; await asyncio.sleep(0.5)
        await main_menu.handle_main_view(self, callback_query)
        await callback_query.answer()
test_menu = test()

class main_menu:
    def __init__(self):
        router.callback_query(F.data == "main_view")(self.handle_main_view)
        router.callback_query(F.data == "support")(self.handle_support)
        router.callback_query(F.data == "equip")(self.handle_equip)
        router.callback_query(F.data == "neuro")(self.handle_neuro)
        router.callback_query(F.data == "room")(self.handle_room)
        router.callback_query(F.data == "test")(self.hand_test)

    async def hand_test(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Тут кнопки с разными вариантами обновления, какой больше нравится ?", reply_markup=kb_test())
        await callback_query.answer()


    async def handle_main_view(self, callback_query: CallbackQuery):
        pictireFile = open('resources/mein_picture').read().strip()
        text = ("Выберите опцию: "
                "\n    🖨 - хранилище инструкций "
                "\n    🎨 - Открывает диалог с нейронной сетью"
                "\n    🎮 - Комнаты для обучения"
                "\n    ⛑ - Связь с разработчиками, предложка идей")
        await callback_query.message.answer_photo(
            photo=pictireFile,
            caption=text,
            reply_markup=kb_main_view()
        )
        await callback_query.answer()

    async def handle_equip(self, callback_query: CallbackQuery):
        await callback_query.message.edit_text(
            text="Вы выбрали: Оборудование"
        )
        await callback_query.answer()

    async def handle_neuro(self, callback_query: CallbackQuery):
        await callback_query.message.edit_text(
            text="Запускается режим общения с нейронной сетью, напишите стоп, что бы из него выйти"
        )
        await callback_query.answer()

    async def handle_room(self, callback_query: CallbackQuery):
        await callback_query.message.edit_text(
            text="Вы выбрали: Комнаты"
        )
        await callback_query.answer()

    async def handle_support(self, callback_query: CallbackQuery):
        await callback_query.message.edit_text(
            text="Вы выбрали: Поддержка", reply_markup=kb_sup_view()
        )
        await callback_query.answer()
main_menu_class = main_menu()

class room_menu_main:
    def __init__(self):
        router.callback_query(F.data == "room_teach")(self.handle_room_teach)
        router.callback_query(F.data == "room_stud")(self.handle_room_stud)

    async def handle_room_teach(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Выберите темы и задания")
        await callback_query.answer()

    async def handle_room_stud(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Впишите код для подключения к комнате")
        await callback_query.answer()

room_menu_main_class = room_menu_main()

class sup_menu:
    def __init__(self):
        router.callback_query(F.data == "sup_idea")(self.handle_sup_idea)
        router.callback_query(F.data == "sup_mis")(self.handle_sup_mis)

    async def handle_sup_idea(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Напишите в сообщении ниже вашу идею, она будет переданна разработчикам")
        await callback_query.answer()

    async def handle_sup_mis(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Напишите в сообщении ниже: название, категория оборудования и какие ошибки допущены при составлении инструкии")
        await callback_query.answer()
sup_menu_class = sup_menu()

