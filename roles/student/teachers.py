from flask import Blueprint
from credentials import bot
from database.grade import Grade
from database.subject import Subject
from database.subject_debtor import SubjectDebtor
import os

teachers = Blueprint('teachers', __name__)


@teachers.route('/teachers')
def teachers_schelude(message):
    file_name = 'Розклад викладачів'
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tmp/'

    doc = open(f'{file_path}{file_name}.xls', 'rb')

    bot.send_document(chat_id=message.from_user.id, data=doc)

    bot.send_message(chat_id=374464076, text='#asked_teachers')


def get_grades(message):
    print()

    grades_dict = {}

    for grade in Grade.get_grade_by_student(student_id=message.from_user.id):
        subject = Subject.get_subject_by_id(grade.subject_id)
        grade = grade.grade

        grades_dict.setdefault(subject, []).append(grade)

    grades = '<b>Оцінки</b>:\n'
    for subject in grades_dict:
        grades += ''.join(f'{subject}: {", ".join(grades_dict[subject])}\n')

    debts = '\n<b>Борги</b>:\n'
    debts += '\n'.join([Subject.get_subject_by_id(debt.subject_id) for debt in SubjectDebtor.get_debt_by_student(student_id=message.from_user.id)])

    bot.send_message(chat_id=message.from_user.id, text=grades+debts, parse_mode='html')
