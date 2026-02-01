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

class main_menu:
    def main_menu_view(self):
        keyboard_main = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🖨 - Оборудование", callback_data="equip")],
                [InlineKeyboardButton(text="🎨 - Чат с ИИ-помощником", callback_data="neuro")],
                [InlineKeyboardButton(text="🎮 - Тесты и комнаты", callback_data="room")],
                [InlineKeyboardButton(text="⛑ - Обратная связь", callback_data="support")],
            ]
        )
        return keyboard_main

    def kb_sup_view(self):
        keyboard_sup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📩 - Предложить идею", callback_data="sup_idea")],
                [InlineKeyboardButton(text="⛑ - Сообщить об ошибке", callback_data="sup_mis")],
                [InlineKeyboardButton(text="🧲 - Назад", callback_data="main_view")]
            ]
        )
        return keyboard_sup

    def sup_in_back(self):
        keyboard_sup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🧲 - Отмена", callback_data="support")]
            ]
        )
        return keyboard_sup

    def kb_room_view(self):
        keyboard_room = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Создать", callback_data="room_create")],
                [InlineKeyboardButton(text="Присоединиться", callback_data="room_join")],
                [InlineKeyboardButton(text="Самостоятельное выполнение", callback_data="room_solo")],
                [InlineKeyboardButton(text="🧲 - Назад", callback_data="main_view")]
            ]
        )
        return keyboard_room
kbBase_main_menu = main_menu()

class equips_menu:
    def equips_menu(self):
        keyboard_equip_mainMenu = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Автономные роботы", callback_data="equipMenu_autRob")],
                [InlineKeyboardButton(text="Лего роботы", callback_data="equipMenu_legoRob")],
                [InlineKeyboardButton(text="Стационарные/настольные", callback_data="equipMenu_stanc")],
                [InlineKeyboardButton(text="БПЛА", callback_data="equipMenu_BPLA")],
                [InlineKeyboardButton(text="3D Принтеры", callback_data="equipMenu_3Dprint")],
                [InlineKeyboardButton(text="Резаки", callback_data="equipMenu_rez")],
                [InlineKeyboardButton(text="🧲 - Назад", callback_data="main_view")]
            ]
        )
        return keyboard_equip_mainMenu

    class robots:
        def kb_equipMenu_autRobots(self):
            keyboard_equipMenu_autRobots = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Пушка/без пушки", callback_data="equipMenu_autRob_Push")],
                    [InlineKeyboardButton(text="🧲 - Назад", callback_data="equip")]
                ]
            )
            return keyboard_equipMenu_autRobots

        def kb_equipMenu_legoRobots(self):
            keyboard_equipMenu_legoRobots = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Железный набор", callback_data="equipMenu_legoRob_iron")],
                    [InlineKeyboardButton(text="Электрический' набор", callback_data="equipMenu_legoRob_electro")],
                    [InlineKeyboardButton(text="Железно-Электрический набор",
                                          callback_data="equipMenu_legoRob_electroIron")],
                    [InlineKeyboardButton(text="🧲 - Назад", callback_data="equip")]
                ]
            )
            return keyboard_equipMenu_legoRobots

#    robots = robots()

    class stacion:
        def kb_equipMenu_stacion(self):
            keyboard_equipMenu_stacion = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Палка", callback_data="equipMenu_autRob")],
                    [InlineKeyboardButton(text="Светофор", callback_data="equipMenu_legoRob")],
                    [InlineKeyboardButton(text="Сортировщик", callback_data="equipMenu_stanc")],
                    [InlineKeyboardButton(text="🧲 - Назад", callback_data="equip")]
                ]
            )
            return keyboard_equipMenu_stacion

#    stacion = stacion()

    class BPLA:
        def kb_equipMenu_BPLA(self):
            keyboard_equipMenu_BPLA = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Дрон", callback_data="equipMenu_BPLA_dron")],
                    [InlineKeyboardButton(text="🧲 - Назад", callback_data="equip")]
                ]
            )
            return keyboard_equipMenu_BPLA

#    BPLA = BPLA()

    class D3printer:
        def kb_equipMenu_D3printer(self):
            keyboard_equipMenu_D3printer = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Треугольный", callback_data="equipMenu_D3printer_trian")],
                    [InlineKeyboardButton(text="Квадратный", callback_data="equipMenu_D3printer_squa")],
                    [InlineKeyboardButton(text="🧲 - Назад", callback_data="equip")]
                ]
            )
            return keyboard_equipMenu_D3printer

#    D3printer = D3printer()

    class rezak:
        def kb_equipMenu_rezak(self):
            keyboard_equipMenu_rezak = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="По дереву", callback_data="equipMenu_rezak_trees")],
                    [InlineKeyboardButton(text="🧲 - Назад", callback_data="equip")]
                ]
            )
            return keyboard_equipMenu_rezak
kbBase_equip_main_menu = equips_menu()
#    rezak = rezak()
# equips_menu = equips_menu()