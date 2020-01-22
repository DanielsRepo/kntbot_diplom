from flask import Blueprint
from credentials import *
from db.group import Group
from db.student import Student, Debtor
from keyboard import make_keyboard
from helpers import restricted
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

debtors = Blueprint('debtors', __name__)


@debtors.route('/debtors')
def debtor_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='Добавить должника', callback_data='add_debtor'))
    keyboard.add(InlineKeyboardButton(text='Удалить должника', callback_data='delete_debtor'))
    keyboard.add(InlineKeyboardButton(text='Должники по группе', callback_data='debtors_of_group'))

    bot.send_message(message.from_user.id, text='Выбери', reply_markup=keyboard)


@bot.message_handler(commands=['debt'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_debtor'))
@restricted
# add debtor
def debt(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'debtorgroup_')

    bot.send_message(message.from_user.id, text='Группа', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtorgroup_'))
def group_callback(call):
    group_id = call.data.split('_')[1]

    students = [student for student in Student.get_students_by_group(group_id)]

    student_keyboard = make_keyboard('student', students, f'debtor_{Group.get_group_by_id(group_id)}_')

    bot.send_message(call.from_user.id, text='Кто должник', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtor_'))
def group_callback(call):
    group = call.data.split('_')[1]
    debtor_id = call.data.split('_')[2]

    Debtor.add_debtor(debtor_id)

    bot.send_message(call.from_user.id, text=f'Студент {Student.get_student_by_id(debtor_id).name} группы {group} занесен в должники')


# delete debtor
@bot.message_handler(commands=['deldebt'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_debtor'))
@restricted
def delete_debt(message):
    debtor_keyboard = make_keyboard('student', Debtor.get_all_debtors(), f'deldebtor_')

    bot.send_message(message.from_user.id, text='Кого убрать', reply_markup=debtor_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('deldebtor_'))
def group_callback(call):
    debtor_id = call.data.split('_')[1]

    bot.send_message(call.from_user.id, text=f'Студент {Student.get_student_by_id(debtor_id).name} группы {Group.get_group_by_id(Student.get_student_by_id(debtor_id).group_id)} удален из должников')

    Debtor.delete_debtor(debtor_id)


# get debtors
@bot.message_handler(commands=['grdebt'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('debtors_of_group'))
@restricted
def get_debtors_by_group(message):
    group_list = Group.get_groups()

    group_keyboard = make_keyboard('group', group_list, 'grdebtor_')

    bot.send_message(message.from_user.id, text='Должники какой группы', reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('grdebtor_'))
def group_callback(call):
    group_id = call.data.split('_')[1]
    debtors = ''
    for debtor in Debtor.get_debtors_by_group(group_id):
        debtors += debtor + '\n'

    bot.send_message(call.from_user.id, text=f'Должники группы {Group.get_group_by_id(group_id)}:\n{debtors}')

