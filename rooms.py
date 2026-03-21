# rooms.py
import logging
import random
import string
from typing import Dict, List, Optional

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from inlineKeyBoard_db import kbBase_main_menu
from tests import tests

logger = logging.getLogger(__name__)
wait_router_rooms = Router()


class roomStates(StatesGroup):
    roomKeySOLOSwait = State()
    roomKeyWait = State()
    roomNameWait = State()

class roomSolo:
    def __init__(self):
        self.sessions = {}

    def regUser(self, user_id: int):
        if user_id not in self.sessions:
            questions = tests['Техника безопасности']['questions']
            self.sessions[user_id] = {
                'score': 0,
                'quest_now': 0,
                'total_quest': len(questions),
                'chat_id': None,
                'message_id': None,
                'room_mode': False,
                'room_key': None,
            }

    async def send_question(self, user_id: int, bot, edit: bool = False):
        data = self.sessions[user_id]
        q_index = data['quest_now']
        questions = tests['Техника безопасности']['questions']
        q_data = questions[q_index]
        text = q_data['text']
        options = q_data['options']

        buttons = [[InlineKeyboardButton(text=opt, callback_data=f"answer_{i}")] for i, opt in enumerate(options)]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        if edit and data['message_id']:
            try:
                await bot.edit_message_text(
                    chat_id=data['chat_id'],
                    message_id=data['message_id'],
                    text=f"❓ {text}\n\nВыберите правильный ответ:",
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.warning(f"Failed to edit message: {e}")
                msg = await bot.send_message(
                    chat_id=data['chat_id'] if data['chat_id'] else user_id,
                    text=f"❓ {text}\n\nВыберите правильный ответ:",
                    reply_markup=keyboard
                )
                data['chat_id'] = msg.chat.id
                data['message_id'] = msg.message_id
                self.sessions[user_id] = data
        else:
            msg = await bot.send_message(
                chat_id=data['chat_id'] if data['chat_id'] else user_id,
                text=f"❓ {text}\n\nВыберите правильный ответ:",
                reply_markup=keyboard
            )
            data['chat_id'] = msg.chat.id
            data['message_id'] = msg.message_id
            self.sessions[user_id] = data
solo = roomSolo()


class Room:
    def __init__(self, key: str, name: str, owner_id: int, owner_name: str):
        self.key = key
        self.name = name
        self.owner_id = owner_id
        self.members = {owner_id}
        self.names = {owner_id: owner_name}
        self.ready = {owner_id: True}
        self.topic = list(tests.keys())[0]
        self.results = {}  # {user_id: {'score': int, 'total': int}}

rooms = {}
user_to_room = {}
user_lobby_msg = {}

def generate_key() -> str:
    return ''.join(random.choices(string.digits, k=6))

async def update_lobby(room: Room, user_id: int, bot, edit: bool = True):
    lines = [
        f"Название: {room.name}",
        f"Тема: {room.topic}",
        f"🔑 Код-join: <code>{room.key}</code>",
        "Участники:"
    ]
    for uid in sorted(room.members):
        status = "✅" if room.ready.get(uid, False) else "❌"
        owner_mark = "👑 " if uid == room.owner_id else ""
        name = room.names.get(uid, str(uid))
        result_str = ""
        if uid in room.results:
            res = room.results[uid]
            result_str = f" ({res['score']}/{res['total']})"
        lines.append(f"  {status} {name} {owner_mark}{result_str}")
    text = "\n".join(lines)

    buttons = []
    is_ready = room.ready.get(user_id, False)
    buttons.append([InlineKeyboardButton(
        text="🟢 Готов" if is_ready else "🔴 Не готов",
        callback_data=f"lobby_toggle_{room.key}"
    )])
    buttons.append([InlineKeyboardButton(text="🚪 Выйти", callback_data=f"lobby_exit_{room.key}")])
    if user_id == room.owner_id:
        buttons.append([InlineKeyboardButton(text="📖 Выбрать тему", callback_data=f"lobby_topic_{room.key}")])
        buttons.append([InlineKeyboardButton(text="▶️ Запустить тест", callback_data=f"lobby_start_{room.key}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    if edit and user_id in user_lobby_msg:
        chat_id, msg_id = user_lobby_msg[user_id]
        try:
            await bot.edit_message_text(text, chat_id=chat_id, message_id=msg_id, reply_markup=keyboard, parse_mode="HTML")
            return
        except Exception as e:
            logger.warning(f"Failed to edit lobby for {user_id}: {e}")
            del user_lobby_msg[user_id]
    msg = await bot.send_message(user_id, text, reply_markup=keyboard, parse_mode="HTML")
    user_lobby_msg[user_id] = (msg.chat.id, msg.message_id)

async def update_lobby_for_others(room: Room, bot, exclude_user_id: int):
    for uid in room.members:
        if uid != exclude_user_id:
            await update_lobby(room, uid, bot, edit=True)

def get_cancel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_action")
    ]])

@wait_router_rooms.callback_query(lambda c: c.data == "room_create")
async def create_room_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(roomStates.roomNameWait)
    kb = get_cancel_keyboard()
    if callback.message.text:
        await callback.message.edit_text("Введите название комнаты:", reply_markup=kb)
    else:
        await callback.message.answer("Введите название комнаты:", reply_markup=kb)
    await callback.answer()

@wait_router_rooms.callback_query(lambda c: c.data == "room_join")
async def join_room_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(roomStates.roomKeyWait)
    kb = get_cancel_keyboard()
    if callback.message.text:
        await callback.message.edit_text("🔑 Введите код комнаты:", reply_markup=kb)
    else:
        await callback.message.answer("🔑 Введите код комнаты:", reply_markup=kb)
    await callback.answer()

@wait_router_rooms.callback_query(lambda c: c.data == "room_test-safety")
async def start_solo(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(roomStates.roomKeySOLOSwait)
    solo.regUser(user_id)
    solo.sessions[user_id]['chat_id'] = callback.message.chat.id
    await solo.send_question(user_id, callback.bot, edit=False)
    await callback.answer()

@wait_router_rooms.callback_query(lambda c: c.data == "cancel_action")
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if callback.message.text:
        await callback.message.edit_text("Действие отменено.")
    else:
        await callback.message.answer("Действие отменено.")
    await callback.message.answer("Главное меню:", reply_markup=kbBase_main_menu)
    await callback.answer()

# Ввод кода румы
@wait_router_rooms.message(roomStates.roomNameWait)
async def process_room_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Название не может быть пустым. Попробуйте ещё раз:", reply_markup=get_cancel_keyboard())
        return
    user_id = message.from_user.id
    if user_id in user_to_room:
        await message.answer("Вы уже находитесь в комнате. Выйдите из текущей, чтобы создать новую.")
        await state.clear()
        return
    key = generate_key()
    user_name = message.from_user.full_name
    room = Room(key, name, user_id, user_name)
    rooms[key] = room
    user_to_room[user_id] = key
    await update_lobby(room, user_id, message.bot, edit=False)
    await state.clear()

@wait_router_rooms.message(roomStates.roomKeyWait)
async def process_room_key(message: Message, state: FSMContext):
    key = message.text.strip()
    user_id = message.from_user.id
    if user_id in user_to_room:
        await message.answer("Вы уже в комнате. Выйдите сначала.")
        await state.clear()
        return
    room = rooms.get(key)
    if not room:
        await message.answer("Комната не найдена. Проверьте код.", reply_markup=get_cancel_keyboard())
        return
    user_name = message.from_user.full_name
    room.members.add(user_id)
    room.names[user_id] = user_name
    room.ready[user_id] = False
    user_to_room[user_id] = key
    await update_lobby(room, user_id, message.bot, edit=False)
    await update_lobby_for_others(room, message.bot, user_id)
    await state.clear()


@wait_router_rooms.callback_query(lambda c: c.data.startswith("lobby_toggle_"))
async def toggle_ready(callback: CallbackQuery):
    key = callback.data.split("_")[2]
    user_id = callback.from_user.id
    room = rooms.get(key)
    if not room or user_id not in room.members:
        await callback.answer("Комната не найдена", show_alert=True)
        return
    room.ready[user_id] = not room.ready.get(user_id, False)
    for uid in room.members:
        await update_lobby(room, uid, callback.bot, edit=True)
    await callback.answer()

@wait_router_rooms.callback_query(lambda c: c.data.startswith("lobby_exit_"))
async def exit_room(callback: CallbackQuery):
    key = callback.data.split("_")[2]
    user_id = callback.from_user.id
    room = rooms.get(key)
    if not room:
        await callback.answer("Комната не найдена", show_alert=True)
        return
    if user_id == room.owner_id:
        for uid in list(room.members):
            user_to_room.pop(uid, None)
            if uid in user_lobby_msg:
                try:
                    await callback.bot.delete_message(*user_lobby_msg[uid])
                except:
                    pass
                del user_lobby_msg[uid]
        del rooms[key]
        await callback.answer("Комната удалена")
    else:
        room.members.discard(user_id)
        room.ready.pop(user_id, None)
        room.names.pop(user_id, None)
        user_to_room.pop(user_id, None)
        if user_id in user_lobby_msg:
            try:
                await callback.bot.delete_message(*user_lobby_msg[user_id])
            except:
                pass
            del user_lobby_msg[user_id]
        for uid in room.members:
            await update_lobby(room, uid, callback.bot, edit=True)
        await callback.answer("Вы вышли из комнаты")
    await callback.message.delete()

@wait_router_rooms.callback_query(lambda c: c.data.startswith("lobby_topic_"))
async def select_topic(callback: CallbackQuery):
    key = callback.data.split("_")[2]
    user_id = callback.from_user.id
    room = rooms.get(key)
    if not room or user_id != room.owner_id:
        await callback.answer("Доступно только владельцу", show_alert=True)
        return
    topics = list(tests.keys())
    buttons = [[InlineKeyboardButton(text=t, callback_data=f"set_topic_{key}_{i}")] for i, t in enumerate(topics)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text("Выберите тему теста:", reply_markup=keyboard)

@wait_router_rooms.callback_query(lambda c: c.data.startswith("set_topic_"))
async def set_topic(callback: CallbackQuery):
    parts = callback.data.split("_")
    key = parts[2]
    topic_index = int(parts[3])
    user_id = callback.from_user.id
    room = rooms.get(key)
    if not room or user_id != room.owner_id:
        await callback.answer("Ошибка", show_alert=True)
        return
    room.topic = list(tests.keys())[topic_index]
    for uid in room.members:
        await update_lobby(room, uid, callback.bot, edit=True)
    await callback.answer(f"Тема установлена: {room.topic}")

@wait_router_rooms.callback_query(lambda c: c.data.startswith("lobby_start_"))
async def start_room_test(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split("_")[2]
    user_id = callback.from_user.id
    room = rooms.get(key)
    if not room or user_id != room.owner_id:
        await callback.answer("Доступно только владельцу", show_alert=True)
        return
    participants = [uid for uid in room.members if uid != room.owner_id]
    if not participants:
        await callback.answer("Нет участников для теста", show_alert=True)
        return
    for uid in participants:
        if uid in user_lobby_msg:
            try:
                await callback.bot.delete_message(*user_lobby_msg[uid])
            except:
                pass
            del user_lobby_msg[uid]
        solo.regUser(uid)
        solo.sessions[uid]['room_key'] = key
        solo.sessions[uid]['room_mode'] = True
        solo.sessions[uid]['chat_id'] = uid
        storage_key = StorageKey(bot_id=callback.bot.id, user_id=uid, chat_id=uid)
        await state.storage.set_state(key=storage_key, state=roomStates.roomKeySOLOSwait)
        await solo.send_question(uid, callback.bot, edit=False)
    await callback.answer("Тест запущен!")

# Ответы квушн
@wait_router_rooms.callback_query(StateFilter(roomStates.roomKeySOLOSwait))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id not in solo.sessions:
        await callback.answer("Тест не найден. Начните заново.", show_alert=True)
        return

    data = solo.sessions[user_id]
    if not callback.data.startswith("answer_"):
        await callback.answer()
        return

    answer_index = int(callback.data.split("_")[1])
    current_q = data['quest_now']
    questions = tests['Техника безопасности']['questions']
    correct_index = questions[current_q]['correct']

    if answer_index == correct_index:
        data['score'] += 1

    data['quest_now'] += 1
    solo.sessions[user_id] = data

    if data['quest_now'] < data['total_quest']:
        await solo.send_question(user_id, callback.bot, edit=True)
    else:
        score = data['score']
        total = data['total_quest']

        if data.get('room_mode'):
            room_key = data['room_key']
            room = rooms.get(room_key)
            if room:
                room.results[user_id] = {'score': score, 'total': total}
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="Вернуться в лобби", callback_data=f"back_to_lobby_{room_key}")
                ]])
                await callback.bot.edit_message_text(
                    chat_id=data['chat_id'],
                    message_id=data['message_id'],
                    text=f"Тест завершён!\nВаш результат: {score} из {total}",
                    reply_markup=kb
                )
                await update_lobby(room, room.owner_id, callback.bot, edit=True)

            storage_key = StorageKey(bot_id=callback.bot.id, user_id=user_id, chat_id=user_id)
            await state.storage.set_state(key=storage_key, state=None)
            del solo.sessions[user_id]
        else:
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Выйти в меню", callback_data="room")
            ]])
            await callback.bot.edit_message_text(
                chat_id=data['chat_id'],
                message_id=data['message_id'],
                text=f"Тест завершён!\nВаш результат: {score} из {total}",
                reply_markup=kb
            )
            del solo.sessions[user_id]
            await state.clear()

    await callback.answer()

@wait_router_rooms.callback_query(lambda c: c.data.startswith("back_to_lobby_"))
async def back_to_lobby(callback: CallbackQuery):
    key = callback.data.split("_")[3]
    user_id = callback.from_user.id
    room = rooms.get(key)
    if not room or user_id not in room.members:
        await callback.answer("Комната не найдена", show_alert=True)
        return
    await callback.message.delete()
    await update_lobby(room, user_id, callback.bot, edit=False)
    await callback.answer()