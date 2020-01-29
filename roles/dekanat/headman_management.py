from flask import Blueprint
from credentials import *
from db.headman import Headman
from db.group import Group
from db.dekanat import Dekanat
from db.student import Student
from keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

headman_management = Blueprint('headman_management', __name__)


@headman_management.route('/headman_management')
@bot.message_handler(commands=['ratehead'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('assign_headman'))
def rate_headman(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'rateheadman_')

    bot.send_message(message.from_user.id, text='Староста группы', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('rateheadman_'))
def rate_headman_callback(call):
    group_id = call.data.split('_')[1]

    headman = Headman.get_headman_by_group(group_id)

    headman_rate_keyboard = InlineKeyboardMarkup()
    headman_rate_keyboard.row(
        InlineKeyboardButton(text='-', callback_data=f'rateminus_{group_id}'),
        InlineKeyboardButton(text=f'{headman.rating}', callback_data=f'{headman}'),
        InlineKeyboardButton(text='+', callback_data=f'rateplus_{group_id}')
    )

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Староста группы КНТ-{Group.get_group_by_id(group_id)} {Student.get_student_by_id(headman.student_id).name}',
                          reply_markup=headman_rate_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('rateminus_'))
def rate_headman_minus_callback(call):
    group_id = call.data.split('_')[1]

    headman = Headman.get_headman_by_group(group_id)

    Dekanat.rate_headman(group_id, '-')

    headman_rate_keyboard = InlineKeyboardMarkup()
    headman_rate_keyboard.row(
        InlineKeyboardButton(text='-', callback_data=f'rateminus_{group_id}'),
        InlineKeyboardButton(text=f'{headman.rating}', callback_data='headrate_'),
        InlineKeyboardButton(text='+', callback_data=f'rateplus_{group_id}')
    )

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Староста группы КНТ-{Group.get_group_by_id(group_id)} {Student.get_student_by_id(headman.student_id).name}',
                          reply_markup=headman_rate_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('rateplus_'))
def rate_headman_plus_callback(call):
    group_id = call.data.split('_')[1]

    headman = Headman.get_headman_by_group(group_id)

    Dekanat.rate_headman(group_id, '+')

    headman_rate_keyboard = InlineKeyboardMarkup()
    headman_rate_keyboard.row(
        InlineKeyboardButton(text='-', callback_data=f'rateminus_{group_id}'),
        InlineKeyboardButton(text=f'{headman.rating}', callback_data=f'{headman}'),
        InlineKeyboardButton(text='+', callback_data=f'rateplus_{group_id}')
    )

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Староста группы КНТ-{Group.get_group_by_id(group_id)} {Student.get_student_by_id(headman.student_id).name}',
                          reply_markup=headman_rate_keyboard)