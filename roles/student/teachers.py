from flask import Blueprint
from credentials import bot

teachers = Blueprint('teachers', __name__)


@teachers.route('/teachers')
def teachers_schelude(message):
    file_name = 'Розклад кафедри ПЗ 2 сем. 2019-2020'
    doc = open(f'./tmp/{file_name}.xls', 'rb')

    bot.send_document(chat_id=message.from_user.id, data=doc)
