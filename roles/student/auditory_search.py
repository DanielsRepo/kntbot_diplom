from flask import Blueprint
from credentials import *
from db.audience import Audience
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

auditory_search = Blueprint('auditory_search', __name__)


@auditory_search.route('/auditory_search')
def search_aud(message):
    Audience.add_aud()
    auds = ' '.join(i.number for i in Audience.get_all_aud())
    bot.send_message(chat_id=message.from_user.id, text=f'Введи номер потрібної аудиторії\n{auds}')

    bot.register_next_step_handler(message, get_aud)


def get_aud(message):
    number = message.text

    search_again = InlineKeyboardMarkup()
    search_again.add(InlineKeyboardButton(text=f'{emojize(":mag_right:", use_aliases=True)} Шукати ще',
                                          callback_data='search_aud_again'))

    if Audience.get_aud(number) is None:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Аудиторію не знайдено {emojize(":white_frowning_face:", use_aliases=True)}',
                         reply_markup=search_again)
    else:
        building, floor = Audience.get_aud(number)
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Аудиторія: {number}\nКорпус: {building}\nПоверх: {floor}',
                         reply_markup=search_again)


@bot.callback_query_handler(func=lambda call: call.data.startswith('search_aud_again'))
def search_aud_again(call):
    Audience.add_aud()
    auds = ' '.join(i.number for i in Audience.get_all_aud())

    message = bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=f'Введи номер потрібної аудиторії\n{auds}')

    bot.register_next_step_handler(message, get_aud)
