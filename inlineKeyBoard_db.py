from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_test():
    keyboard_test = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отправка нового", callback_data="1")],
            [InlineKeyboardButton(text="Редактируется", callback_data="2")],
            [InlineKeyboardButton(text="Удаляет ждет отправляет", callback_data="3")],
            [InlineKeyboardButton(text="Лоадинг", callback_data="4")]
        ]
    )
    return keyboard_test

def kb_main_view():
    keyboard_main = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="🖨 - Оборудование", callback_data="equip")],
                [InlineKeyboardButton(text="🎨 - Нейро-подсказка", callback_data="neuro")],
                [InlineKeyboardButton(text="🎮 - Комнаты", callback_data="room")],
                [InlineKeyboardButton(text="⛑ - Обратная связь", callback_data="support")],
                [InlineKeyboardButton(text="test", callback_data="test")]
            ]
    )
    return keyboard_main


def kb_sup_view():
    keyboard_sup = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="📩 - Предложить идею", callback_data="sup_idea")],
                [InlineKeyboardButton(text="⛑ - Сообщить об ошибке", callback_data="sup_mis")],
                [InlineKeyboardButton(text="🧲 - Назад", callback_data="main_view")]
            ]
    )
    return keyboard_sup

def kb_room_view():
    keyboard_room = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="📩 - Предложить идею", callback_data="sup_idea")],
                [InlineKeyboardButton(text="⛑ - Сообщить об ошибке", callback_data="sup_mis")],
                [InlineKeyboardButton(text="🧲 - Назад", callback_data="main_view")]
            ]
    )
    return keyboard_room

