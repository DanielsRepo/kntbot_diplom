from flask import Blueprint
from credentials import bot
from database.group import Group
from database.student import Student
from database.subject import Subject
from database.grade import Grade
from keyboards.keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

grades = Blueprint('grades', __name__)


@grades.route('/grades')
# ADD GRADE
def assign_grade(message):
    subjects_keyboard = InlineKeyboardMarkup(row_width=1)
    keys_list = []
    for elem in Subject.get_subjects():
        keys_list.append(InlineKeyboardButton(text=str(elem.name), callback_data='gradesubject_' + str(elem.id)))
    subjects_keyboard.add(*keys_list)

    bot.send_message(chat_id=message.from_user.id,
                     text='Виберіть предмет:',
                     reply_markup=subjects_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('gradesubject_'))
def choose_subject_callback(call):
    subject_id = call.data.split('_')[1]

    group_keyboard = InlineKeyboardMarkup(row_width=1)
    keys_list = []

    for group in Group.get_groups()[:4]:
        keys_list.append(InlineKeyboardButton(text=str(group.name), callback_data=f'studentsgroup_{subject_id}_' + str(group.id)))

    group_keyboard.add(*keys_list)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть групу:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('studentsgroup_'))
def choose_group_callback(call):
    subject_id = call.data.split('_')[1]
    group_id = call.data.split('_')[2]

    student_keyboard = make_keyboard(keyboard_type='student',
                                     elem_list=[student for student in Student.get_students_by_group(group_id)],
                                     marker=f'gradestudent_{subject_id}_{group_id}_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть студента:',
                          reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('gradestudent_'))
def choose_student_callback(call):
    subject_id = call.data.split('_')[1]
    group_id = call.data.split('_')[2]
    student_id = call.data.split('_')[3]

    student = Student.get_student_by_id(student_id)
    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'<b>Предмет:</b> {Subject.get_subject_by_id(subject_id)}\n'
                               f'<b>Студент:</b> {student.name}\n'
                               f'<b>Група:</b> КНТ-{Group.get_group_by_id(group_id)}\n'
                               f'Яка оцінка?',
                          parse_mode='html')

    bot.register_next_step_handler_by_chat_id(call.from_user.id, add_grade, student_id, subject_id)


def add_grade(message, student_id, subject_id):
    grade = message.text

    Grade.add_grade(grade, student_id, subject_id)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'Оцінку було поставлено {emojize(":white_check_mark:", use_aliases=True)}')

    bot.send_message(chat_id=374464076, text=f'<b>{Subject.get_subject_by_id(subject_id)}</b>: {grade}', parse_mode='html')