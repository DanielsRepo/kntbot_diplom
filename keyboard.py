from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from helpers import LIST_OF_ADMINS
from emoji import emojize


buttons = [
    f'{emojize(":bell:", use_aliases=True)} Расписание звонков',
    f'{emojize(":computer:", use_aliases=True)} Сайт НУЗП',
    f'{emojize(":mag_right:", use_aliases=True)} Поиск аудиторий',
    f'{emojize(":tada:", use_aliases=True)} Мероприятия',
    f'{emojize(":moneybag:", use_aliases=True)} Преподаватели',
    f'{emojize(":beer:", use_aliases=True)} Меню студдекана'
]


def make_menu_keyboard(message):
    menu_keyboard = ReplyKeyboardMarkup(True, False)
    for button in buttons[:5]:
        menu_keyboard.add(button)

    if message.from_user.id in LIST_OF_ADMINS:
        menu_keyboard.add(buttons[5])

    return menu_keyboard


studdekan_buttons = [
    f'{emojize(":poop:", use_aliases=True)} Старосты',
    f'{emojize(":skull:", use_aliases=True)} Должники',
    f'{emojize(":fire:", use_aliases=True)} Организация мероприятий',
    f'{emojize(":back:", use_aliases=True)} Назад'
]

studdekan_keyboard = ReplyKeyboardMarkup(True, False)
for button in studdekan_buttons:
    studdekan_keyboard.add(button)


def make_keyboard(keyboard_type, elem_list, marker):
    keyboard = InlineKeyboardMarkup()
    keys_list = []

    for elem in elem_list:
        keys_list.append(InlineKeyboardButton(text=elem.name, callback_data=marker + str(elem.id)))

    if keyboard_type == 'event' or keyboard_type == 'student':
        keyboard.add(*keys_list)
    elif keyboard_type == 'group':
        i = 0
        j = 7
        for _ in range(len(keys_list)):
            keyboard.row(*keys_list[i:j])
            i += 7
            j += 7

    return keyboard

