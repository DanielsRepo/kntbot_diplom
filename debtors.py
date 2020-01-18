from flask import Blueprint
from credentials import *
from db.group import Group
from db.student import Student, Debtor
from keyboard import make_keyboard

debtors = Blueprint('debtors', __name__)


@debtors.route('/debtors')
@bot.message_handler(commands=['debt'])
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


@bot.message_handler(commands=['deldebt'])
def delete_debt(message):
    debtor_keyboard = make_keyboard('student', Debtor.get_all_debtors(), f'deldebt_')

    bot.send_message(message.from_user.id, text='Кого убрать', reply_markup=debtor_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('deldebt_'))
def group_callback(call):
    debtor_id = call.data.split('_')[1]

    bot.send_message(call.from_user.id, text=f'Студент {Student.get_student_by_id(debtor_id).name} группы {Group.get_group_by_id(Student.get_student_by_id(debtor_id).group_id)} удален из должников')

    Debtor.delete_debtor(debtor_id)


