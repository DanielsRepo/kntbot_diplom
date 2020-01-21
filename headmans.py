from flask import Blueprint
from credentials import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.group import Group
from db.student import Student, Headman
from keyboard import make_keyboard

headmans = Blueprint('headmans', __name__)


@headmans.route('/headmans')
# add headman
@bot.message_handler(commands=['star'])
def star(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'headmangroup_')

    bot.send_message(message.from_user.id, text='Группа', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('headmangroup_'))
def group_callback(call):
    group_id = call.data.split('_')[1]

    student_keyboard = make_keyboard('student', Student.get_students_by_group(group_id), f'headman_{Group.get_group_by_id(group_id)}_')

    bot.send_message(call.from_user.id, text='Кто староста', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('headman_'))
def student_callback(call):
    group = call.data.split('_')[1]
    headman_id = call.data.split('_')[2]

    Headman.add_headman(headman_id)

    bot.send_message(call.from_user.id, text=f'{Student.get_student_by_id(headman_id).name} назначен старостой группы {group}')


# change headman
@bot.message_handler(commands=['chstar'])
def change_star(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'chstargroup_')

    bot.send_message(message.from_user.id, text='Изменить старосту группы', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('chstargroup_'))
def group_callback(call):
    group_id = call.data.split('_')[1]

    student_keyboard = make_keyboard('student', Student.get_students_by_group(group_id), f'chheadman_{Group.get_group_by_id(group_id)}_')

    bot.send_message(call.from_user.id, text='Кто новый староста', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('chheadman_'))
def student_callback(call):
    group = call.data.split('_')[1]
    new_headman_id = call.data.split('_')[2]

    Headman.change_headman(new_headman_id)

    bot.send_message(call.from_user.id, text=f'{Student.get_student_by_id(new_headman_id).name} назначен старостой группы {group}')


# get headman
@bot.message_handler(commands=['getstar'])
def get_star(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'getstargroup_')

    bot.send_message(message.from_user.id, text='Глянуть старосту группы', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('getstargroup_'))
def group_callback(call):
    group_id = call.data.split('_')[1]

    headman = Headman.get_headman_by_group(group_id)

    bot.send_message(call.from_user.id, text=f'{Student.get_student_by_id(headman.id).name}')

