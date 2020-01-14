from flask import Blueprint
from credentials import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.group import Group
from db.student import Student

registration = Blueprint('registration', __name__)


@registration.route('/registration')
@bot.message_handler(commands=['reg'])
def register(message):
    # Group.add_groups()
    group_keyboard = InlineKeyboardMarkup()
    group_list = []
    for group in Group.get_groups():
        if len(group_list) != 7:
            group_list.append(InlineKeyboardButton(text=group.group, callback_data='group_' + group.group))
        else:
            group_keyboard.row(*group_list)
            group_list.clear()

    bot.send_message(message.from_user.id, text='Группа', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_'))
def group_callback(call):
    group = call.data.split('_')[1]
    Student.add_user(call.from_user.id)
    Student.update_user(id=call.from_user.id, group_id=Group.get_id_by_group(group))

    message = bot.send_message(call.from_user.id, 'ФИО')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text

    Student.update_user(id=message.from_user.id, name=name)

    message = bot.send_message(message.from_user.id, 'номер телефона')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    phone = message.text

    Student.update_user(id=message.from_user.id, phone=phone)

    user = Student.get_user(message.from_user.id)

    success_message = f'''
        Регистрация студента {user.name}
        с мобилой {user.phone}
        группы {Group.get_group_by_id(user.group_id)}
        на удивление прошла успешно
    '''
    bot.send_message(message.from_user.id, success_message)