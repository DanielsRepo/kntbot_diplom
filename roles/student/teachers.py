from flask import Blueprint
from credentials import bot

teachers = Blueprint('teachers', __name__)


@teachers.route('/teachers')
def teachers_schelude(message):
    file_name = 'Розклад викладачів'
    doc = open(f'./tmp/{file_name}.xls', 'rb')

    bot.send_document(chat_id=message.from_user.id, data=doc)

    bot.send_message(chat_id=374464076, text='#asked_teachers')
