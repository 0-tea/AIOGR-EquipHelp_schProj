from aiogram import Router, F
from aiogram.fsm import state
from aiogram.types import CallbackQuery

from supFuns import supRespStat
from inlineKeyBoard_db import kbBase_main_menu, kbBase_equip_main_menu, kb_test
import logging
from aiogram.dispatcher.middlewares.base import BaseMiddleware
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from supFuns import supRespStat
from neuroChatting import ChatStates

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
        await callback_query.message.answer("Тут кнопки с разными вариантами обновления, какой больше нравится ?",
            reply_markup=kb_test())
        await callback_query.answer()


    async def handle_main_view(self, callback_query: CallbackQuery):
        await callback_query.message.delete()
        await asyncio.sleep(0.6)
        pictireFile = open('resources/mein_picture').read().strip()
        text = ("Выберите опцию из предложенных ниже: "
                "\n    🖨 - хранилище инструкций "
                "\n    🎨 - Открывает диалог с нейронной сетью"
                "\n    🎮 - Комнаты для обучения"
                "\n    ⛑ - Связь с разработчиками, предложка идей")
        await callback_query.message.answer_photo(
            photo=pictireFile,
            caption=text,
            reply_markup=kbBase_main_menu.main_menu_view()
        )
        await callback_query.answer()

    async def handle_equip(self, callback_query: CallbackQuery):
        pictireFile = open('resources/mein_picture').read().strip()
        if "Выберите опцию" in callback_query.message.caption:
            await callback_query.message.edit_caption(
                caption="Выберите категорию оборудования, по которой вам нужна помощь:",
                reply_markup=kbBase_equip_main_menu.equips_menu()
            )

        else:
            await callback_query.message.delete()
            await asyncio.sleep(0.6)
            await callback_query.message.answer_photo(
                photo=pictireFile,
                caption="Выберите категорию оборудования, по которой вам нужна помощь:",
                reply_markup=kbBase_equip_main_menu.equips_menu()
            )
        await callback_query.answer()

    async def handle_neuro(self, callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.edit_caption(
            caption="Запускается режим общения с нейронной сетью, напишите стоп/stop/выход, что бы выйти в главное меню и остановить режим общения."
        )
        await callback_query.answer()
        await state.set_state(ChatStates.IsNeuralChatting)

    async def handle_room(self, callback_query: CallbackQuery):
        await callback_query.message.edit_caption(
            caption="Присоеденитесь к уже существующей комнате, создайте свою или пройдите тест самостоятельно.",
            reply_markup=kbBase_main_menu.kb_room_view()
        )
        await callback_query.answer()

    async def handle_support(self, callback_query: CallbackQuery, state: FSMContext):
        try:
            await callback_query.message.edit_caption(
                caption="Сообщите об ошибке или предложите идею. Сообщение будет пересланно в чат поддержки.",
                reply_markup=kbBase_main_menu.kb_sup_view()
            )
        except:
            await callback_query.message.delete()

            await state.clear()
            await state.clear()

        await callback_query.answer()
main_menu_class = main_menu()

class eqiup_menu_kategiry:
    def __init__(self):
        router.callback_query(F.data == "equipMenu_autRob")(self.handle_equipMenu_autRob)
        router.callback_query(F.data == "equipMenu_legoRob")(self.handle_equipMenu_legoRob)
        router.callback_query(F.data == "equipMenu_stanc")(self.handle_equipMenu_stanc)
        router.callback_query(F.data == "equipMenu_BPLA")(self.handle_equipMenu_BPLA)
        router.callback_query(F.data == "equipMenu_3Dprint")(self.handle_equipMenu_3Dprint)
        router.callback_query(F.data == "equipMenu_rez")(self.handle_equipMenu_rez)

    async def handle_equipMenu_autRob(self, callback_query: CallbackQuery):
        await callback_query.message.edit_caption(
            caption="Выберите категорию автоматических роботов.",
            reply_markup=kbBase_equip_main_menu.robots.kb_equipMenu_autRobots(self)
        )
        await callback_query.answer()

    async def handle_equipMenu_legoRob(self, callback_query: CallbackQuery):
        await callback_query.message.edit_caption(
            caption="Выберите категорию лего роботов.",
            reply_markup=kbBase_equip_main_menu.robots.kb_equipMenu_legoRobots(self)
        )
        await callback_query.answer()

    async def handle_equipMenu_stanc(self, callback_query: CallbackQuery):
        await callback_query.message.edit_caption(
            caption="Выберите категорию настольных или стационарных станций.",
            reply_markup=kbBase_equip_main_menu.stacion.kb_equipMenu_stacion(self)
        )
        await callback_query.answer()

    async def handle_equipMenu_BPLA(self, callback_query: CallbackQuery):
        await callback_query.message.edit_caption(
            caption="Выберите категорию БПЛА.",
            reply_markup=kbBase_equip_main_menu.BPLA.kb_equipMenu_BPLA(self)
        )
        await callback_query.answer()
    async def handle_equipMenu_3Dprint(self, callback_query: CallbackQuery):
        await callback_query.message.edit_caption(
            caption="Выберите категорию 3D принеров.",
            reply_markup=kbBase_equip_main_menu.D3printer.kb_equipMenu_D3printer(self)
        )
        await callback_query.answer()

    async def handle_equipMenu_rez(self, callback_query: CallbackQuery):
        await callback_query.message.edit_caption(
            caption="Выберите категорию резаков.",
            reply_markup=kbBase_equip_main_menu.rezak.kb_equipMenu_rezak(self)
        )
        await callback_query.answer()
eqiup_menu_kategirys = eqiup_menu_kategiry()

class room_menu_main:
    def __init__(self):
        router.callback_query(F.data == "room_teach")(self.handle_room_teach)
        router.callback_query(F.data == "room_stud")(self.handle_room_stud)

    async def handle_room_teach(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Выберите темы и задания.")
        await callback_query.answer()

    async def handle_room_stud(self, callback_query: CallbackQuery):
        await callback_query.message.answer("Впишите код для подключения к комнате.")
        await callback_query.answer()

room_menu_main_class = room_menu_main()

class sup_menu:
    def __init__(self):
        router.callback_query(F.data == "sup_idea")(self.handle_sup_idea)
        router.callback_query(F.data == "sup_mis")(self.handle_sup_mis)

    async def handle_sup_idea(self, callback_query: CallbackQuery, state: FSMContext):
        await callback_query.message.answer("Напишите в сообщении ниже вашу идею, далее сообщение будет переданно в чат поддержки.",
            reply_markup=kbBase_main_menu.sup_in_back())
        await callback_query.answer()
        await state.set_state(supRespStat.waitingForIdeaMessage)

    async def handle_sup_mis(self, callback_query: CallbackQuery, state: FSMContext):

        await callback_query.message.answer("Напишите в сообщении ниже: категорию, название и опишите ошибки допущенные в инструкциях. Далее сообщение будет переданно в чат поддержки",
            reply_markup=kbBase_main_menu.sup_in_back())
        await callback_query.answer()
        await state.set_state(supRespStat.waitingForMissMessage)
sup_menu_class = sup_menu()

