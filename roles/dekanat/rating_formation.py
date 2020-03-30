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

            score = calculate_score(student.id)
            if score is False:
                continue
            else:
                stud_dict[name_group] = [score[0], score[1], score[2]]
        except AttributeError:
            continue

    return stud_dict


def calculate_score(student_id):
    coef = 0.9

    subject_quantity = len(Subject.get_subjects())

    grade_sum_hundred_system = sum([int(grade.grade) for grade in Grade.get_grades_by_student(student_id)])
    grade_sum_five_system = sum([convert_to_five(int(grade.grade)) for grade in Grade.get_grades_by_student(student_id)])

    extragrade = sum([int(exgrade.extra_grade) for exgrade in ExtraGrade.get_extragrade_by_student(student_id)])

    score_hundred_system = coef * (grade_sum_hundred_system / subject_quantity) + extragrade
    score_five_system = grade_sum_five_system / subject_quantity

    if score_hundred_system < 60:
        return False
    else:
        return [score_five_system, score_hundred_system, extragrade]


def convert_to_five(score):
    if score >= 90:
        return 5
    elif score >= 75:
        return 4
    elif score >= 60:
        return 3
    elif score >= 60:
        return 2
    else:
        return 1
