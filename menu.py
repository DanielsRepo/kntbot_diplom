from flask import Blueprint, session
from credentials import *
from keyboard import menu_keyboard
from db.db import db, conn

from db.audience import Audience
from db.event import Event, EventVisitor
from db.student import Student, Headman, Debtor
from db.group import Group


menu = Blueprint('menu', __name__)


@menu.route('/menu')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'LETS GO', reply_markup=menu_keyboard)


@bot.message_handler(commands=['del'])
def delete(message):
    # Audience.__table__.drop()

    print("DELETED")
    db.delete()


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.from_user.id, "я не знаю как тебе помочь")


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Пока")
#     elif message.text == buttons[0]:
#         bot.send_photo(message.from_user.id, "https://image.winudf.com/v2/image1/Y29tLnJ1c2xhbnRlcmVzaGNoZW5rby5zdHVkZHlfc2NyZWVuXzJfMTU1NDAwODQzN18wNjU/screen-2.jpg?fakeurl=1&type=.jpg")
#     elif message.text == buttons[1]:
#         bot.send_message(message.from_user.id, "http://www.zntu.edu.ua")
#     elif message.text == buttons[2]:
#         search_aud(message)
#     else:
#         bot.send_message(message.from_user.id, "Отвали или обратись за помощью /help.")