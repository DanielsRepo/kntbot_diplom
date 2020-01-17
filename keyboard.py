from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

buttons = [
    'Расписание звонков',
    'Сайт НУЗП',
    'Поиск аудиторий'
]

menu_keyboard = ReplyKeyboardMarkup(True, True)
menu_keyboard.row(*buttons)


def make_keyboard(elem_list, marker):
    keyboard = InlineKeyboardMarkup()
    keys_list = []
    for elem in elem_list:
        keys_list.append(InlineKeyboardButton(text=elem.name, callback_data=marker + str(elem.id)))
    keyboard.add(*keys_list)

    return keys_list, keyboard


def make_event_keyboard(event_list, marker):
    group_keys_list, group_keyboard = make_keyboard(event_list, marker)
    group_keyboard.add(*group_keys_list)

    return group_keys_list, group_keyboard


def make_group_keyboard(group_list, marker):
    # group_keys_list, group_keyboard = make_keyboard(group_list, marker)
    group_keyboard = InlineKeyboardMarkup()
    group_keys_list = []
    for elem in group_list:
        group_keys_list.append(InlineKeyboardButton(text=elem, callback_data=marker + elem))

    i = 0
    j = 7
    for _ in range(len(group_keys_list)):
        group_keyboard.row(*group_keys_list[i:j])
        i += 7
        j += 7

    return group_keyboard

