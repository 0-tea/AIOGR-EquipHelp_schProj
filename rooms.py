from typing import Dict, List
import asyncio
import logging
from typing import Dict, List
from aiogram import types
import requests
from aiogram import Router
from aiogram.types import Update, InlineKeyboardMarkup, InlineKeyboardButton
from inlineKeyBoard_db import kbBase_main_menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
import os

from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
import logging
from aiogram import Router

from tests import tests

load_dotenv('tokens.env')
logger = logging.getLogger(__name__)
wait_router_rooms = Router()

class roomStates(StatesGroup):
    roomKeySOLOSwait = State()
    roomKeyWait = State()
    roomNameWait = State()

class roomSolo:
    def __init__(self):
        self.sessions = {}

    def regUser(self, message: types.Message):

        if self.session.get(message.from_user.id) is None:
            self.session[message.from_user.id] = {'score': 0, 'numb_questions': 0}


    @wait_router_rooms.message(roomStates.roomKeySOLOSwait)
    async def testingSOLO(self, message: types.Message):
        self.regUser(message)
        question_data = tests['Техника безопасности']['questions'][0]
        question_text = question_data['text']
        options = question_data['options']
        correct_answer_index = question_data['correct']

        keyboard = InlineKeyboardMarkup(row_width=1)

        for i, option in enumerate(options):
            # Создаем кнопку с callback_data, содержащей индекс ответа
            button = InlineKeyboardButton(
                text=option,
                callback_data=f"answer_{i}"  # передаем индекс выбранного ответа
            )
            keyboard.add(button)

        await message.answer(
            text=f"❓ {question_text}\n\nВыберите правильный ответ:",
            reply_markup=keyboard
        )









'''
class ROOMS:






    def __init__(self):
        self.roomKey = roomKey
        self.dataMembr: Dict[int, List[dict]] = {}
        '''  '''

    def
'''