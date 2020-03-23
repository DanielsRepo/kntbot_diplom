from flask import Blueprint
from credentials import bot
from keyboards.keyboard import make_keyboard, make_role_replykeyboard, studdekan_buttons
from database.group import Group
from database.student import Student
from database.extra_grade import ExtraGrade
from emoji import emojize


extragrade_assignment = Blueprint('extragrade_assignment', __name__)


@extragrade_assignment.route('/extragrade_assignment')
def add_extragrade(message):

    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='extragradegroup_')

    bot.send_message(chat_id=message.from_user.id,
                     text='Вибери групу:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(message.from_user.id, extragrade_group_callback)


def extragrade_group_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        student_keyboard = make_keyboard(keyboard_type='student',
                                         elem_list=[student for student in Student.get_students_by_group(group_id)],
                                         marker=f'extragradestudent_')

        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери студента:', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('extragradestudent_'))
def extragrade_student_callback(call):
    student_id = call.data.split('_')[1]

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Введи додатковий бал (1-10)')

    bot.register_next_step_handler_by_chat_id(call.from_user.id, add_extragrade_func, student_id)


def add_extragrade_func(message, student_id):
    ExtraGrade.add_extragrade(extra_grade=int(message.text), student_id=student_id)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'Додатковий бал було поставлено {emojize(":white_check_mark:", use_aliases=True)}')

    bot.send_message(chat_id=message.from_user.id,
                     text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(studdekan_buttons))
