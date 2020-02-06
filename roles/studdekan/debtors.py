from flask import Blueprint
from credentials import *
from db.group import Group
from db.student import Student
from db.debtor import Debtor
from keyboard import make_keyboard
from helpers import restricted_studdekan
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

debtors = Blueprint('debtors', __name__)


@debtors.route('/debtors')
def debtor_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Додати боржника {emojize(":heavy_plus_sign:", use_aliases=True)}',
                                      callback_data='add_debtor'))
    keyboard.add(InlineKeyboardButton(text=f'Видалити боржника {emojize(":heavy_minus_sign:", use_aliases=True)}',
                                      callback_data='delete_debtor'))
    keyboard.add(InlineKeyboardButton(text=f'Боржники за групою {emojize(":busts_in_silhouette:", use_aliases=True)}',
                                      callback_data='debtors_of_group'))

    bot.send_message(message.from_user.id, text='Вибери дію:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_debtor'))
@restricted_studdekan
# add debtor
def add_debtor(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='debtorgroup_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Вибери групу:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtorgroup_'))
def debtor_group_callback(call):
    group_id = call.data.split('_')[1]

    student_keyboard = make_keyboard(keyboard_type='student',
                                     elem_list=[student for student in Student.get_students_by_group(group_id)],
                                     marker=f'debtor_{Group.get_group_by_id(group_id)}_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Вибери студента:', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtor_'))
def add_debtor_callback(call):
    group = call.data.split('_')[1]
    debtor_id = call.data.split('_')[2]

    Debtor.add_debtor(debtor_id)

    username = Student.get_student_by_id(debtor_id).username
    name = Student.get_student_by_id(debtor_id).name

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Студент <a href="t.me/{username}">{name}</a> '
                               f'групи {group} занесений до боржників',
                          parse_mode='html')


# delete debtor
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_debtor'))
@restricted_studdekan
def delete_debtor(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='deldebtorgroup_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Вибери групу:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('deldebtorgroup_'))
def delete_debtor_group_callback(call):
    group_id = call.data.split('_')[1]

    debtor_list = Debtor.get_debtors_by_group(group_id)
    debtor_list_keyboard = InlineKeyboardMarkup()

    if not debtor_list:
        message_text = 'В цій групі немає боржників'
    else:
        debtor_list_keyboard = make_keyboard(keyboard_type='student',
                                             elem_list=debtor_list,
                                             marker='deldebtor_')
        message_text = 'Вибери боржника:'

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=message_text,
                          reply_markup=debtor_list_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('deldebtor_'))
def delete_debtor_callback(call):
    debtor_id = call.data.split('_')[1]

    group = Group.get_group_by_id(Student.get_student_by_id(debtor_id).group_id)
    username = Student.get_student_by_id(debtor_id).username
    name = Student.get_student_by_id(debtor_id).name

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Студент <a href="t.me/{username}">{name}</a> '
                               f'групи {group} видалений з боржників',
                          parse_mode='html')

    Debtor.delete_debtor(debtor_id)


# get debtors
@bot.callback_query_handler(func=lambda call: call.data.startswith('debtors_of_group'))
@restricted_studdekan
def get_debtors_by_group(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='grdebtor_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Вибери групу:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('grdebtor_'))
def get_debtors_by_group_callback(call):
    group_id = call.data.split('_')[1]
    group = Group.get_group_by_id(group_id)

    debtors_list = Debtor.get_debtors_by_group(group_id)

    if not debtors_list:
        message_text = 'В цій групі немає боржників'
    else:
        debtors_str = ''.join((f'<a href="t.me/{debtor.username}">{debtor.name}</a>\n' for debtor in debtors_list))
        message_text = f'Боржники групи {group}:\n{debtors_str}'

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=message_text,
                          parse_mode='html',
                          disable_web_page_preview=True)

