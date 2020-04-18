from flask import Blueprint
from credentials import bot
from database.subject import Subject
from database.grade_type import GradeType
from database.grade import Grade
from database.subject_debtor import SubjectDebtor
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from keyboards.keyboard import make_keyboard
import os

studying = Blueprint('studying', __name__)


@studying.route('/studying')
def show_studying_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Методичні матеріали {emojize(":books:", use_aliases=True)}',
                                      callback_data='study_methods'))
    keyboard.add(InlineKeyboardButton(text=f'Моя успішність {emojize(":chart_with_upwards_trend:", use_aliases=True)}',
                                      callback_data='my_progress'))

    bot.send_message(message.from_user.id, text='Вибери:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('study_methods'))
def get_subject(call):
    subjects_keyboard = make_keyboard('subject', Subject.get_subjects(), 'getfilesubject_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Вибери предмет:',
                          reply_markup=subjects_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('getfilesubject_'))
def get_study_methods(call):
    subject_id = call.data.split('_')[1]
    subject_name = Subject.get_subject_by_id(subject_id)

    subject_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + f'/tmp/{subject_name}'
    if os.path.exists(subject_path) and os.listdir(subject_path):
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text=f'Методичні матеріали по предмету {subject_name}')

        for file_name in next(os.walk(subject_path))[2]:
            doc = open(f'{subject_path}/{file_name}', 'rb')
            bot.send_document(chat_id=call.from_user.id, data=doc)
    else:
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text='Методичних матеріалів немає')


@bot.callback_query_handler(func=lambda call: call.data.startswith('my_progress'))
def get_my_progress(call):
    grades_dict = {}

    for grade in Grade.get_grades_by_student(student_id=call.from_user.id):
        subject = Subject.get_subject_by_id(grade.subject_id)
        grade_type = GradeType.get_gradetype_by_id(grade.gradetype_id)
        ects = grade.ects
        grade = grade.grade

        grades_dict.setdefault(subject, []).append(f' {grade_type}: {grade} ({ects})\n')

    grades = '<b>Оцінки</b>:\n\n'

    for subject in grades_dict:
        grades += ''.join(f'<i>{subject}:</i>\n{"".join(grades_dict[subject])}\n')

    debts = '<b>Борги</b>: '
    debts += ', '.join([Subject.get_subject_by_id(debt.subject_id)
                        for debt in SubjectDebtor.get_debt_by_student(student_id=call.from_user.id)])

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=grades+debts, parse_mode='html')
