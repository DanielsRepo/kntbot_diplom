from flask import Blueprint
from credentials import bot
from database.grade import Grade
from database.extra_grade import ExtraGrade

from database.group import Group
from database.student import Student
from database.subject import Subject
from helpers.xlsx_helper import make_student_grades_table, get_fio
import os
from pprint import pprint

rating_formation = Blueprint('rating_formation', __name__)


@rating_formation.route('/rating_formation')
@bot.callback_query_handler(func=lambda call: call.data.startswith('create_rating'))
def create_rating(message):
    file_name = 'Рейтинг'
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tmp/'

    stud_dict = prepare_student_grades_table()

    make_student_grades_table(stud_dict=stud_dict, file_name=file_name, file_path=file_path)

    doc = open(f'{file_path}{file_name}.xlsx', 'rb')

    bot.send_message(chat_id=message.from_user.id, text='Документ з рейтингом студентів')
    bot.send_document(chat_id=message.from_user.id, data=doc)


def prepare_student_grades_table():
    stud_dict = {}

    for student in Student.get_all_students():
        try:
            name_group = f'{student.name}_{Group.get_group_by_id(student.group_id)}'

            score, extragrade = calculate_score(student.id)

            stud_dict[name_group] = [convert_score(score), score, extragrade]
        except AttributeError:
            continue

    return stud_dict


def calculate_score(student_id):
    max_rating_score = 100
    max_subject_score = 100

    subject_score = sum([int(grade.grade) for grade in Grade.get_grades_by_student(student_id)])
    subject_quantity = len(Subject.get_subjects())

    extragrade = sum([int(exgrade.extra_grade) for exgrade in ExtraGrade.get_extragrade_by_student(student_id)])

    score = max_rating_score * (subject_score / (subject_quantity * max_subject_score)) + extragrade

    return score, extragrade


def convert_score(score):
    if score >= 90:
        return 5
    elif score >= 80:
        return 4
    elif score >= 70:
        return 3
    elif score >= 60:
        return 2
    else:
        return 1
