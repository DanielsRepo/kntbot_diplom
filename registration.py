from flask import Blueprint
from credentials import *
from db.group import Group
from db.student import Student
from keyboard import make_group_keyboard

registration = Blueprint('registration', __name__)


@registration.route('/registration')
@bot.message_handler(commands=['reg'])
def register(message):
    Group.add_groups()
    Student.add_students()

    group_keyboard = make_group_keyboard(Group.get_groups(), 'group_')

    bot.send_message(message.from_user.id, text='Группа', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_'))
def group_callback(call):
    group = call.data.split('_')[1]
    Student.add_student(call.from_user.id)
    Student.update_student(student_id=call.from_user.id, group_id=Group.get_id_by_group(group))

    message = bot.send_message(call.from_user.id, 'ФИО')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text

    Student.update_student(student_id=message.from_user.id, name=name)

    message = bot.send_message(message.from_user.id, 'номер телефона')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    phone = message.text

    Student.update_student(student_id=message.from_user.id, phone=phone)

    user = Student.get_student_by_id(message.from_user.id)

    success_message = f'''
        Регистрация студента {user.name}
        с мобилой {user.phone}
        группы {Group.get_group_by_id(user.group_id)}
        на удивление прошла успешно
    '''
    bot.send_message(message.from_user.id, success_message)