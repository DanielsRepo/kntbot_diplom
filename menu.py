from flask import Blueprint, session
from keyboard import make_menu_keyboard, menu_buttons, make_role_replykeyboard, studdekan_buttons, headman_buttons, dekanat_buttons
from db.db import db, conn
from roles.student.auditory_search import search_aud
from roles.student.events import get_events_schelude
from roles.studdekan.headmans import headman_keyboard
from roles.studdekan.debtors import debtor_keyboard
from roles.studdekan.event_organize import event_organize_keyboard
from roles.studdekan.event_visits import event_visits_keyboard
from roles.dekanat.headman_management import rate_headman, remind_journal, send_file
from credentials import *
from helpers import restricted_studdekan, restricted_headman
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = Blueprint('menu', __name__)


@menu.route('/menu')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=make_menu_keyboard(message))


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in menu_buttons)
def get_student_messages(message):
    if message.text == menu_buttons[0]:
        bot.send_photo(message.from_user.id, "https://image.winudf.com/v2/image1/Y29tLnJ1c2xhbnRlcmVzaGNoZW5rby5zdHVkZHlfc2NyZWVuXzJfMTU1NDAwODQzN18wNjU/screen-2.jpg?fakeurl=1&type=.jpg")
    elif message.text == menu_buttons[1]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='http://www.zntu.edu.ua', url='http://www.zntu.edu.ua'))
        bot.send_message(message.chat.id, 'Сайт НУЗП', reply_markup=markup)
    elif message.text == menu_buttons[2]:
        search_aud(message)
    elif message.text == menu_buttons[3]:
        get_events_schelude(message)
    elif message.text == menu_buttons[4]:
        bot.send_message(message.from_user.id, "Пока ниче")
    elif message.text == menu_buttons[5]:
        show_studdekan_keyboard(message)
    elif message.text == menu_buttons[6]:
        show_headman_keyboard(message)
    elif message.text == menu_buttons[7]:
        show_dekanat_keyboard(message)
    elif message.text == menu_buttons[8]:
        start_message(message)


@bot.message_handler(commands=['studdekan'])
@restricted_studdekan
def show_studdekan_keyboard(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=make_role_replykeyboard(studdekan_buttons))


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in studdekan_buttons)
@restricted_studdekan
def get_studdekan_messages(message):
    if message.text == studdekan_buttons[0]:
        headman_keyboard(message)
    elif message.text == studdekan_buttons[1]:
        debtor_keyboard(message)
    elif message.text == studdekan_buttons[2]:
        event_organize_keyboard(message)
    elif message.text == studdekan_buttons[3]:
        event_visits_keyboard(message)


@bot.message_handler(commands=['headman'])
@restricted_headman
def show_headman_keyboard(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=make_role_replykeyboard(headman_buttons))


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in headman_buttons)
@restricted_headman
def get_headman_messages(message):
    if message.text == headman_buttons[0]:
        print('1')
    elif message.text == headman_buttons[1]:
        print('2')
    elif message.text == headman_buttons[2]:
        start_message(message)


@bot.message_handler(commands=['dekanat'])
def show_dekanat_keyboard(message):
    bot.send_message(message.from_user.id, 'Выберите пункт меню:', reply_markup=make_role_replykeyboard(dekanat_buttons))


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in dekanat_buttons)
def get_dekanat_messages(message):
    if message.text == dekanat_buttons[0]:
        rate_headman(message)
    elif message.text == dekanat_buttons[1]:
        remind_journal(message)
    elif message.text == dekanat_buttons[2]:
        send_file(message)


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


