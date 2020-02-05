from flask import Blueprint
from credentials import *
from db.headman import Headman
from db.group import Group
from db.dekanat import Dekanat
from db.student import Student
from keyboard import make_keyboard, make_headman_rate_keyboard
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

headman_management = Blueprint('headman_management', __name__)


@headman_management.route('/headman_management')
@bot.message_handler(commands=['ratehead'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('assign_headman'))
def rate_headman(message):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='rateheadman_')

    bot.send_message(chat_id=message.from_user.id, text='Староста группы', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('rateheadman_'))
def rate_headman_callback(call):
    group_id = call.data.split('_')[1]
    group = Group.get_group_by_id(group_id)

    headman = Headman.get_headman_by_group(group_id)
    headman_name = Student.get_student_by_id(headman.student_id).name

    headman_rate_keyboard = make_headman_rate_keyboard(group_id=group_id, rating=headman.rating)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Староста групи КНТ-{group} {headman_name}',
                          reply_markup=headman_rate_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith(('rateminus_', 'rateplus_')))
def rate_headman_minus_callback(call):
    group_id = call.data.split('_')[1]
    group = Group.get_group_by_id(group_id)

    headman = Headman.get_headman_by_group(group_id)
    headman_name = Student.get_student_by_id(headman.student_id).name

    if call.data.startswith('rateminus_'):
        Dekanat.rate_headman(group_id, '-')
    elif call.data.startswith('rateplus_'):
        Dekanat.rate_headman(group_id, '+')

    headman_rate_keyboard = make_headman_rate_keyboard(group_id, headman.rating)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Староста групи КНТ-{group} {headman_name}',
                          reply_markup=headman_rate_keyboard)


@bot.message_handler(commands=['remind'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_journal'))
def remind_journal(message):
    remind_keyboard = InlineKeyboardMarkup()

    remind_keyboard.add(InlineKeyboardButton(text='Вибрати старосту', callback_data='remind_one'))
    remind_keyboard.add(InlineKeyboardButton(text='Всім', callback_data='remind_all'))

    bot.send_message(message.from_user.id, text='Кому нагадати?', reply_markup=remind_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_one'))
def remind_one(call):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'remindonegroup_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть старосту якої групи:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remindonegroup'))
def remind_one_callback(call):
    group_id = call.data.split('_')[1]
    group = Group.get_group_by_id(group_id)

    headman = Headman.get_headman_by_group(group_id)
    headman_name = Student.get_student_by_id(headman.student_id).name

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Старості групи КНТ-{group} '
                               f'{headman_name} було відправлено нагадування')

    bot.send_message(headman.student_id, 'ЗАПОВНИ ЖУРНАЛ')
    print(headman.student_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_all'))
def remind_all(call):
    for headman_id in Headman.get_all_headmans():
        try:
            bot.send_message(headman_id, text='ЗАПОВНИ ЖУРНАЛ')
        except ApiException:
            continue

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Всім старостам було відправлено нагадування')


@bot.message_handler(commands=['sendf'])
def send_file(message):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='sendfile_')

    bot.send_message(chat_id=message.from_user.id, text='Виберіть старосту групи:', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('sendfile'))
def send_file_callback(call):
    group_id = call.data.split('_')[1]

    headman = Headman.get_headman_by_group(group_id)

    message = bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text='Відправте файл боту і він його передасть старості')

    bot.register_next_step_handler(message, send_file_headman, headman.student_id)


@bot.message_handler(content_types=['document', 'photo'])
def send_file_headman(message, headman_id):
    file_id = message.document.file_id

    bot.send_message(chat_id=message.from_user.id, text='Файл відправлений старості')

    bot.send_document(chat_id=headman_id, data=file_id)
