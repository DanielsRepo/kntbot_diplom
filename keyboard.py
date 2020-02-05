from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from helpers import LIST_OF_ADMINS, LIST_OF_HEADMANS, LIST_OF_DEKANAT
from emoji import emojize


menu_buttons = [
    f'{emojize(":bell:", use_aliases=True)} Расписание звонков',
    f'{emojize(":computer:", use_aliases=True)} Сайт НУЗП',
    f'{emojize(":mag_right:", use_aliases=True)} Поиск аудиторий',
    f'{emojize(":tada:", use_aliases=True)} Мероприятия',
    f'{emojize(":moneybag:", use_aliases=True)} Преподаватели',
    f'{emojize(":iphone:", use_aliases=True)} Меню студдекана',
    f'{emojize(":beer:", use_aliases=True)} Меню старосты',
    f'{emojize(":clipboard:", use_aliases=True)} Меню деканата'
]

studdekan_buttons = [
    f'{emojize(":poop:", use_aliases=True)} Старосты',
    f'{emojize(":dollar:", use_aliases=True)} Должники',
    f'{emojize(":fire:", use_aliases=True)} Организация мероприятий',
    f'{emojize(":busts_in_silhouette:", use_aliases=True)} Посещения мероприятий',
    f'{emojize(":back:", use_aliases=True)} Назад'
]

headman_buttons = [
    f'{emojize(":computer:", use_aliases=True)} headman command 1',
    f'{emojize(":computer:", use_aliases=True)} headman command 2',
    f'{emojize(":back:", use_aliases=True)} Наазад'
]

dekanat_buttons = [
    f'{emojize(":chart_with_upwards_trend:", use_aliases=True)} Рейтинг старосты',
    f'{emojize(":sound:", use_aliases=True)} Напомнить про журналы',
    f'{emojize(":envelope:", use_aliases=True)} Отправить файл',
    f'{emojize(":back:", use_aliases=True)} Назаад'
]


def make_menu_keyboard(message):
    menu_keyboard = ReplyKeyboardMarkup(True, False)
    for button in menu_buttons[:5]:
        menu_keyboard.add(button)

    if message.from_user.id in LIST_OF_ADMINS:
        menu_keyboard.add(menu_buttons[5])

    if message.from_user.id in LIST_OF_HEADMANS:
        menu_keyboard.add(menu_buttons[6])

    if message.from_user.id in LIST_OF_DEKANAT:
        menu_keyboard.add(menu_buttons[7])

    return menu_keyboard


def make_role_replykeyboard(buttons):
    role_keyboard = ReplyKeyboardMarkup(True, False)
    for button in buttons:
        role_keyboard.add(button)

    return role_keyboard


def make_headman_rate_keyboard(group_id, rating):
    headman_rate_keyboard = InlineKeyboardMarkup()
    headman_rate_keyboard.row(
        InlineKeyboardButton(text='-', callback_data=f'rateminus_{group_id}'),
        InlineKeyboardButton(text=f'{rating}', callback_data=f'{rating}'),
        InlineKeyboardButton(text='+', callback_data=f'rateplus_{group_id}')
    )
    return headman_rate_keyboard


def make_keyboard(keyboard_type, elem_list, marker):
    keyboard = InlineKeyboardMarkup(row_width=1)
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


# def make_studdekan_inlinekeyboard(keys_dict):
#     keyboard = InlineKeyboardMarkup(row_width=1)
#
#     for key, value in keys_dict.items():
#         keyboard.add(InlineKeyboardButton(text=key, callback_data=value))
#
#     return keyboard
