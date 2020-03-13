from flask import Blueprint
from credentials import bot
from database.group import Group
from database.student import Student
from keyboards.keyboard import make_keyboard, make_menu_keyboard
from emoji import emojize
import re

registration = Blueprint('registration', __name__)


@registration.route('/registration')
def add_another_fac(message):
    Student.add_student(Student(id=message.from_user.id,
                                username=message.from_user.username,
                                group_id=Group.get_id_by_group('other')))


def register(message):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='group_')

    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)

    bot.send_message(chat_id=message.from_user.id, text='Вибери свою групу:', reply_markup=group_keyboard)
    bot.register_next_step_handler_by_chat_id(message.from_user.id, group_callback)


def group_callback(message):
    group_id = Group.get_id_by_group(message.text)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери свою групу:')

        bot.register_next_step_handler_by_chat_id(message.from_user.id, group_callback)
    else:
        student = Student()
        student.id = message.from_user.id
        student.username = message.from_user.username
        student.group_id = group_id

        message = bot.send_message(chat_id=message.from_user.id, text='Введи Ф.I.O. українською мовою')
        bot.register_next_step_handler(message, get_name, student)


def get_name(message, student):
    name = message.text

    if bool(re.search("[^А-ЯҐЄІIЇа-яiієїґ' -]+", name)) or len(name.split(' ')) != 3 or len(name) > 256:
        message = bot.send_message(chat_id=message.from_user.id,
                                   text='Неккоректний ввід\nВведи Ф.I.O. українською мовою')
        bot.register_next_step_handler(message, get_name, student)
    else:
        student.name = name

        message = bot.send_message(chat_id=message.from_user.id, text='Введи свій номер телефону')
        bot.register_next_step_handler(message, get_phone, student)


def get_phone(message, student):
    phone = message.text

    if bool(re.search("[^0-9+]+", phone)) or len(phone) > 13:
        message = bot.send_message(chat_id=message.from_user.id,
                                   text='Неккоректний ввід\nВведи свій номер телефону')
        bot.register_next_step_handler(message, get_phone, student)
    else:
        student.phone = phone
        student.add_student(student)

        success_message = f'Вітаю, ти зареєстрований {emojize(":white_check_mark:", use_aliases=True)}'
        bot.send_message(chat_id=message.from_user.id, text=success_message,
                         reply_markup=make_menu_keyboard(message, other_fac=False))

        bot.send_message(chat_id=374464076,
                         text=f'#registered <a href="t.me/{student.username}">{student.name}</a> '
                              f'КНТ-{Group.get_group_by_id(student.group_id)}',
                         parse_mode='html',
                         disable_web_page_preview=True)


@bot.message_handler(commands=['reg301198'])
def register_for_admins(message):
    if Student.get_student_by_id(message.from_user.id) is None:
        group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='group_')

        bot.send_message(chat_id=message.from_user.id, text='Вибери свою групу:', reply_markup=group_keyboard)
        bot.register_next_step_handler_by_chat_id(message.from_user.id, group_callback)
    else:
        bot.send_message(chat_id=message.from_user.id, text='Ти вже зареєстрований')
        bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
