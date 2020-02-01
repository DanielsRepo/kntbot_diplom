from flask import Blueprint
from credentials import *
from db.group import Group
from db.student import Student
from db.headman import Headman
from keyboard import make_keyboard
from helpers import restricted_studdekan
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

headmans = Blueprint('headmans', __name__)


@headmans.route('/headmans')
def headman_keyboard(message):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton(text='Призначити старосту', callback_data='assign_headman'))
    keyboard.add(InlineKeyboardButton(text='Змінити старосту', callback_data='change_headman'))
    keyboard.add(InlineKeyboardButton(text='Переглянути старосту', callback_data='get_headman'))

    bot.send_message(message.from_user.id, text='Вибери дію:', reply_markup=keyboard)


# add headman
@bot.message_handler(commands=['addhead'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('assign_headman'))
@restricted_studdekan
def add_headman(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'headmangroup_')

    bot.edit_message_text(chat_id=message.from_user.id,
                          message_id=message.message.message_id,
                          text='Вибери групу:', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('headmangroup_'))
def headman_group_callback(call):
    group_id = call.data.split('_')[1]

    student_keyboard = make_keyboard('student', Student.get_students_by_group(group_id), f'headman_{Group.get_group_by_id(group_id)}_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Вибери старосту:', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('headman_'))
def add_headman_callback(call):
    group = call.data.split('_')[1]
    headman_id = call.data.split('_')[2]

    Headman.add_headman(headman_id)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'{Student.get_student_by_id(headman_id).name} призначений старостою групи {group}')


# change headman
@bot.message_handler(commands=['chhead'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('change_headman'))
@restricted_studdekan
def change_headman(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'chheadgroup_')

    bot.edit_message_text(chat_id=message.from_user.id,
                          message_id=message.message.message_id,
                          text='Изменить старосту группы', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('chheadgroup_'))
def headman_group_callback(call):
    group_id = call.data.split('_')[1]

    student_keyboard = make_keyboard('student', Student.get_students_by_group(group_id), f'chheadman_{Group.get_group_by_id(group_id)}_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Кто новый староста', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('chheadman_'))
def change_headman_callback(call):
    group = call.data.split('_')[1]
    new_headman_id = call.data.split('_')[2]

    Headman.change_headman(new_headman_id)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'{Student.get_student_by_id(new_headman_id).name} назначен старостой группы {group}')


# get headman
@bot.message_handler(commands=['gethead'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('get_headman'))
@restricted_studdekan
def get_headman(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'getheadgroup_')

    bot.edit_message_text(chat_id=message.from_user.id,
                          message_id=message.message.message_id,
                          text='Вибери группу:', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('getheadgroup_'))
def headman_group_callback(call):
    group_id = call.data.split('_')[1]

    headman = Headman.get_headman_by_group(group_id)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Староста групи {Group.get_group_by_id(group_id)} {Student.get_student_by_id(headman.student_id).name}')
