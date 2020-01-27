from flask import Blueprint, session
from keyboard import make_menu_keyboard, buttons, studdekan_keyboard, studdekan_buttons
from db.db import db, conn
from roles.student.auditory_search import search_aud
from roles.student.events import get_events_schelude
from roles.studdekan.headmans import headman_keyboard
from roles.studdekan.debtors import debtor_keyboard
from roles.studdekan.event_organize import event_organize_keyboard, event_visits_keyboard
from credentials import *
from helpers import restricted

menu = Blueprint('menu', __name__)


@menu.route('/menu')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=make_menu_keyboard(message))


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in buttons)
def get_student_messages(message):
    if message.text == buttons[0]:
        bot.send_photo(message.from_user.id, "https://image.winudf.com/v2/image1/Y29tLnJ1c2xhbnRlcmVzaGNoZW5rby5zdHVkZHlfc2NyZWVuXzJfMTU1NDAwODQzN18wNjU/screen-2.jpg?fakeurl=1&type=.jpg")
    elif message.text == buttons[1]:
        bot.send_message(message.from_user.id, "http://www.zntu.edu.ua")
    elif message.text == buttons[2]:
        search_aud(message)
    elif message.text == buttons[3]:
        get_events_schelude(message)
    elif message.text == buttons[4]:
        bot.send_message(message.from_user.id, "Пока ниче")
    elif message.text == buttons[5]:
        studdekan(message)


@bot.message_handler(commands=['studdekan'])
@restricted
def studdekan(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=studdekan_keyboard)


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in studdekan_buttons)
@restricted
def get_studdekan_messages(message):
    if message.text == studdekan_buttons[0]:
        headman_keyboard(message)
    elif message.text == studdekan_buttons[1]:
        debtor_keyboard(message)
    elif message.text == studdekan_buttons[2]:
        event_organize_keyboard(message)
    elif message.text == studdekan_buttons[3]:
        event_visits_keyboard(message)
    elif message.text == studdekan_buttons[4]:
        start_message(message)


@bot.message_handler(commands=['del'])
def delete(message):
    print("DELETED")
    db.delete()


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.from_user.id, "я не знаю как тебе помочь")


@bot.message_handler(func=lambda message: message.content_type == 'text')
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Отвали или обратись за помощью /help.")


