from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def kb_main_view():
    keyboard_main = InlineKeyboardMarkup(
        inline_keyboard=[
                [InlineKeyboardButton(text="[🖨] - Оборудование", callback_data="equip")],
                [InlineKeyboardButton(text="[🎨] - Нейро-подсказка", callback_data="neuro")],
                [InlineKeyboardButton(text="[🎮] - Комнаты", callback_data="room")],
                [InlineKeyboardButton(text="[⛑] - Поддержка", callback_data="support")]
            ]
    )
    return keyboard_main



