from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

buttons = [
    'Расписание звонков',
    'Сайт НУЗП',
    'Поиск аудиторий',
    'Мероприятия'
]

menu_keyboard = ReplyKeyboardMarkup(True, False)
for button in buttons:
    menu_keyboard.add(button)


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

