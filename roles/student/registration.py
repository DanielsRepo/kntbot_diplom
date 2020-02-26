from flask import Blueprint
from credentials import bot
from db.group import Group
from db.student import Student
from keyboard import make_keyboard, make_menu_keyboard
from emoji import emojize
import re

registration = Blueprint('registration', __name__)


@registration.route('/registration')
def add_another_fac(message):
    Student.add_student(message.from_user.id, message.from_user.username)
    Student.update_student(student_id=message.from_user.id, group_id=Group.get_id_by_group('other'))


def register(message):
    if Student.get_student_by_id(message.from_user.id) is None:
        group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='group_')

        bot.send_message(chat_id=message.from_user.id, text='Вибери свою групу', reply_markup=group_keyboard)
    else:
        bot.send_message(chat_id=message.from_user.id, text='Ти вже зареєстрований')

    bot.register_next_step_handler_by_chat_id(message.from_user.id, group_callback)


def group_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id == False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери свою групу')

        bot.register_next_step_handler_by_chat_id(message.from_user.id, group_callback)
    else:
        Student.add_student(message.from_user.id, message.from_user.username)
        Student.update_student(student_id=message.from_user.id, group_id=group_id)

        message = bot.send_message(chat_id=message.from_user.id, text='Введи Ф.I.O. українською мовою')
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text

    if bool(re.search("[^А-ЯҐЄІЇа-яієїґ' -]+", name)) or len(name.split(' ')) != 3:
        message = bot.send_message(chat_id=message.from_user.id,
                                   text='Неккоректний ввід\nВведи Ф.I.O. українською мовою')
        bot.register_next_step_handler(message, get_name)
    else:
        Student.update_student(student_id=message.from_user.id, name=name)

        message = bot.send_message(chat_id=message.from_user.id, text='Введи свій номер телефону')
        bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    phone = message.text

    if bool(re.search("[^0-9]+", phone)):
        message = bot.send_message(chat_id=message.from_user.id,
                                   text='Неккоректний ввід\nВведи свій номер телефону')
        bot.register_next_step_handler(message, get_phone)
    else:
        Student.update_student(student_id=message.from_user.id, phone=phone)

        success_message = f'Вітаю, ти зареєстрований {emojize(":white_check_mark:", use_aliases=True)}'
        bot.send_message(chat_id=message.from_user.id, text=success_message,
                         reply_markup=make_menu_keyboard(message, other_fac=False))
