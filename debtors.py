from flask import Blueprint
from credentials import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.group import Group
from db.student import Student, Debtor
from keyboard import make_group_keyboard, make_keyboard

debtors = Blueprint('debtors', __name__)


@debtors.route('/debtors')
@bot.message_handler(commands=['debt'])
def debt(message):
    group_list = Group.get_groups()

    group_keyboard = make_group_keyboard(group_list, 'debtorgroup_')

    bot.send_message(message.from_user.id, text='Группа', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtorgroup_'))
def group_callback(call):
    group = call.data.split('_')[1]

    keys_list, student_keyboard = make_keyboard(Student.get_students_by_group(Group.get_id_by_group(group)), f'debtor_{group}_')

    bot.send_message(call.from_user.id, text='Кто должник', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtor_'))
def group_callback(call):
    group = call.data.split('_')[1]
    debtor_id = call.data.split('_')[2]

    Debtor.add_debtor(debtor_id)

    bot.send_message(call.from_user.id, text=f'Студент {Student.get_student_by_id(debtor_id).name} группы {group} занесен в должники')


@bot.message_handler(commands=['deldebt'])
def delete_debt(message):
    keys_list, debtor_keyboard = make_keyboard(Debtor.get_all_debtors(), f'deldebt_')

    bot.send_message(message.from_user.id, text='Кого убрать', reply_markup=debtor_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('deldebt_'))
def group_callback(call):
    debtor_id = call.data.split('_')[1]

    Debtor.delete_debtor(debtor_id)

    bot.send_message(call.from_user.id, text=f'УДАЛЕН')

