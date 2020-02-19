from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.role_helpers import LIST_OF_ADMINS, LIST_OF_HEADMANS, LIST_OF_DEKANAT
from emoji import emojize


menu_buttons = [
    f'{emojize(":mag_right:", use_aliases=True)} Пошук аудиторій',
    f'{emojize(":bell:", use_aliases=True)} Розклад дзвоників',
    f'{emojize(":books:", use_aliases=True)} Розклад викладачів',
    f'{emojize(":tada:", use_aliases=True)} Заходи',
    f'{emojize(":computer:", use_aliases=True)} Сайт НУЗП',
    f'{emojize(":briefcase:", use_aliases=True)} Меню студдекана',
    f'{emojize(":notebook_with_decorative_cover:", use_aliases=True)} Меню старости',
    f'{emojize(":clipboard:", use_aliases=True)} Меню деканата',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]

studdekan_buttons = [
    f'{emojize(":ledger:", use_aliases=True)} Старости',
    f'{emojize(":dollar:", use_aliases=True)} Боржники',
    f'{emojize(":calendar:", use_aliases=True)} Організація заходів',
    f'{emojize(":busts_in_silhouette:", use_aliases=True)} Відвідування заходів',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]

headman_buttons = [
    f'{emojize(":computer:", use_aliases=True)} headman command 1',
    f'{emojize(":computer:", use_aliases=True)} headman command 2',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]

dekanat_buttons = [
    f'{emojize(":chart_with_upwards_trend:", use_aliases=True)} Рейтинг старости',
    f'{emojize(":sound:", use_aliases=True)} Нагадати про журнали',
    f'{emojize(":envelope:", use_aliases=True)} Відправити файл',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]


def make_menu_keyboard(message):
    menu_keyboard = ReplyKeyboardMarkup(True, False)
    for button in menu_buttons[:3]:
        menu_keyboard.add(button)
    menu_keyboard.row(*menu_buttons[3:5])

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
