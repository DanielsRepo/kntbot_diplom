from flask import Blueprint
from credentials import bot
from database.group import Group
from database.student import Student
from database.subject import Subject
from database.grade import Grade
from keyboards.keyboard import make_keyboard
from emoji import emojize
from database.subject_debtor import SubjectDebtor

grades = Blueprint('grades', __name__)


@grades.route('/grades')
# ADD GRADE
def assign_grade(message):
    subjects_keyboard = make_keyboard('subject', Subject.get_subjects(), 'gradesubject_')

    bot.send_message(chat_id=message.from_user.id,
                     text='Виберіть предмет:',
                     reply_markup=subjects_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('gradesubject_'))
def choose_subject_callback(call):
    subject_id = call.data.split('_')[1]

    group_keyboard = make_keyboard('student', Group.get_groups()[:4], f'studentsgroup_{subject_id}_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть групу:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('studentsgroup_'))
def choose_group_callback(call):
    subject_id = call.data.split('_')[1]
    group_id = call.data.split('_')[2]

    students = (student for student in Student.get_students_by_group(group_id))

    ask_grade(call, students, subject_id, group_id)


def ask_grade(message, students, subject_id, group_id):
    student = next(students)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'<b>Предмет:</b> {Subject.get_subject_by_id(subject_id)}\n\n'
                          f'<b>Студент:</b> {student.name}\n'
                          f'<b>Група:</b> КНТ-{Group.get_group_by_id(student.group_id)}\n\n'
                          f'Яка оцінка?\n\n'
                          f'Або щоб додати до боржників скористайтеся командою /debt',
                     parse_mode='html')

    bot.register_next_step_handler_by_chat_id(message.from_user.id, add_grade,
                                              students, student.id, subject_id, group_id)


def add_grade(message, students, student_id, subject_id, group_id):
    if message.text == '/cancel':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Дія була скасована {emojize(":white_check_mark:", use_aliases=True)}')
        bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
    elif message.text == '/debt':
        SubjectDebtor.add_debtor(student_id, subject_id)
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Студента було додано до боржників {emojize(":white_check_mark:", use_aliases=True)}')
        ask_grade(message, students, subject_id, group_id)
    else:
        grade = message.text
        Grade.add_grade(grade, student_id, subject_id)

        bot.send_message(chat_id=message.from_user.id,
                         text=f'Оцінку було поставлено {emojize(":white_check_mark:", use_aliases=True)}')

        ask_grade(message, students, subject_id, group_id)
