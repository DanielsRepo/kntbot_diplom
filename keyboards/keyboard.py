from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from helpers.role_helper import LIST_OF_ADMINS, LIST_OF_DEKANAT, LIST_OF_TEACHERS
from emoji import emojize


menu_buttons = [
    f'{emojize(":mag_right:", use_aliases=True)} Пошук аудиторій',
    f'{emojize(":bell:", use_aliases=True)} Розклад дзвінків',
    f'{emojize(":books:", use_aliases=True)} Розклад викладачів',
    f'{emojize(":tada:", use_aliases=True)} Заходи',
    f'{emojize(":computer:", use_aliases=True)} Сайт НУЗП',
    f'{emojize(":chart_with_upwards_trend:", use_aliases=True)} Моя успішність',
    f'{emojize(":briefcase:", use_aliases=True)} Меню студдекана',
    f'{emojize(":clipboard:", use_aliases=True)} Меню деканата',
    f'{emojize(":black_nib:", use_aliases=True)} Меню вчителя',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]

studdekan_buttons = [
    f'{emojize(":ledger:", use_aliases=True)} Старости',
    f'{emojize(":dollar:", use_aliases=True)} Боржники',
    f'{emojize(":calendar:", use_aliases=True)} Організація заходів',
    f'{emojize(":busts_in_silhouette:", use_aliases=True)} Відвідування заходів',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]


teacher_buttons = [
    f'{emojize(":100:", use_aliases=True)} Поставити оцінку',
    f'{emojize(":memo:", use_aliases=True)} Боржники',
    f'{emojize(":notebook_with_decorative_cover:", use_aliases=True)} Відправити методичку',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]

dekanat_buttons = [
    f'{emojize(":chart_with_upwards_trend:", use_aliases=True)} Рейтинг старости',
    f'{emojize(":sound:", use_aliases=True)} Нагадати про журнали',
    f'{emojize(":envelope:", use_aliases=True)} Відправити файл/повідомлення',
    f'{emojize(":arrow_left:", use_aliases=True)} Назад'
]


def make_menu_keyboard(message, other_fac):
    menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=1)

    if other_fac:
        menu_keyboard.add(menu_buttons[0],
                          menu_buttons[1],
                          menu_buttons[3],
                          menu_buttons[4])
    elif message.from_user.id in LIST_OF_ADMINS:
        menu_keyboard.add(menu_buttons[0],
                          menu_buttons[1],
                          menu_buttons[2])
        menu_keyboard.row(menu_buttons[3],
                          menu_buttons[4])
        menu_keyboard.add(menu_buttons[5],
                          menu_buttons[6],
                          menu_buttons[7],
                          menu_buttons[8])
    elif message.from_user.id in LIST_OF_DEKANAT:
        menu_keyboard.add(menu_buttons[0],
                          menu_buttons[1],
                          menu_buttons[4],
                          menu_buttons[7])
    elif message.from_user.id in LIST_OF_TEACHERS:
        menu_keyboard.add(menu_buttons[0],
                          menu_buttons[1],
                          menu_buttons[2],
                          menu_buttons[4],
                          menu_buttons[8])
    else:
        menu_keyboard.add(menu_buttons[0],
                          menu_buttons[1],
                          menu_buttons[2])
        menu_keyboard.row(menu_buttons[3],
                          menu_buttons[4])
        menu_keyboard.add(menu_buttons[5])

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
    if keyboard_type == 'event' or keyboard_type == 'student':
        keyboard = InlineKeyboardMarkup(row_width=1)
        keys_list = []
        for elem in elem_list:
            keys_list.append(InlineKeyboardButton(text=str(elem.name), callback_data=marker + str(elem.id)))

        keyboard.add(*keys_list)
    elif keyboard_type == 'group':
        keyboard = ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)

        keys_list = []

        for elem in elem_list:
            keys_list.append(KeyboardButton(text=str(elem.name)))

        i = 0
        j = 3
        for _ in range(len(keys_list)):
            keyboard.add(*keys_list[i:j])
            i += 3
            j += 3

    return keyboard
