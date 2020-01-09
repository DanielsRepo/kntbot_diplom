from flask import Blueprint
from credentials import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.group import Group
from db.student import Student

registration = Blueprint('registration', __name__)


@registration.route('/registration')
@bot.message_handler(commands=['reg'])
def register(message):
    Group.add_groups()

    group_keyboard = InlineKeyboardMarkup()
    for group in Group.get_groups():
        group_keyboard.add(InlineKeyboardButton(text=group.group, callback_data=group.id))

    bot.send_message(message.from_user.id, text='Группа', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    Student.add_user(call.from_user.id)
    Student.update_user(id=call.from_user.id, group_id=call.data)

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