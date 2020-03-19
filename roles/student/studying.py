from flask import Blueprint
from credentials import bot
from database.subject import Subject
from database.grade import Grade
from database.subject_debtor import SubjectDebtor
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize


studying = Blueprint('studying', __name__)


@studying.route('/studying')
def studying_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Методичні матеріали {emojize(":books:", use_aliases=True)}',
                                      callback_data='study_methods'))
    keyboard.add(InlineKeyboardButton(text=f'Моя успішність {emojize(":chart_with_upwards_trend:", use_aliases=True)}',
                                      callback_data='my_progress'))

    bot.send_message(message.from_user.id, text='Вибери:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('study_methods'))
def get_study_methods(message):
    bot.send_message(chat_id=message.from_user.id, text='study_methods')


@bot.callback_query_handler(func=lambda call: call.data.startswith('my_progress'))
def get_my_progress(message):
    grades_dict = {}

    for grade in Grade.get_grade_by_student(student_id=message.from_user.id):
        subject = Subject.get_subject_by_id(grade.subject_id)
        grade = grade.grade

        grades_dict.setdefault(subject, []).append(grade)

    grades = '<b>Оцінки</b>:\n'
    for subject in grades_dict:
        grades += ''.join(f'{subject}: {", ".join(grades_dict[subject])}\n')

    debts = '\n<b>Борги</b>:\n'
    debts += '\n'.join([Subject.get_subject_by_id(debt.subject_id)
                        for debt in SubjectDebtor.get_debt_by_student(student_id=message.from_user.id)])

    bot.send_message(chat_id=message.from_user.id, text=grades+debts, parse_mode='html')
