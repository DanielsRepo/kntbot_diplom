from flask import Blueprint
from credentials import *
from db.audience import Audience

auditory_search = Blueprint('auditory_search', __name__)


@auditory_search.route('/auditory_search')
@bot.message_handler(commands=['aud'])
def search_aud(message):
    # Audience.add_aud()
    auds = ' '.join(i.number for i in Audience.get_all_aud())
    bot.send_message(message.from_user.id, f'Какая нада аудитория?\n{auds}')

    bot.register_next_step_handler(message, get_aud)


def get_aud(message):
    number = message.text
    building, floor = Audience.get_aud(number)
    bot.send_message(message.from_user.id, f'Аудитория {number} находится в {building} корпусе на {floor} этаже')
