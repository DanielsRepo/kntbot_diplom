from flask import Blueprint, session
from keyboard import make_menu_keyboard, menu_buttons, make_role_replykeyboard, studdekan_buttons, headman_buttons, dekanat_buttons
from db.db import db
from db.group import Group
from db.student import Student
from db.event import Event
from roles.student.auditory_search import search_aud
from roles.student.teachers import teachers_schelude
from roles.student.events import get_events_schelude
from roles.student.registration import register
from roles.studdekan.headmans import headman_keyboard
from roles.studdekan.debtors import debtor_keyboard
from roles.studdekan.event_organize import event_organize_keyboard
from roles.studdekan.event_visits import event_visits_keyboard
from roles.dekanat.headman_management import rate_headman, remind_journal, send_file
from credentials import bot
from helpers.role_helpers import restricted_studdekan, restricted_headman
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

menu = Blueprint('menu', __name__)


@menu.route('/menu')
@bot.message_handler(commands=['start', 'cancel'])
def start_message(message):
    add_all(message)

    # if Student.get_student_by_id(message.from_user.id) is None:
    #     bot.send_message(chat_id=message.from_user.id,
    #                      text=f'Привіт {emojize(":wave:", use_aliases=True)}\n'
    #                           f'Для користування ботом треба зареєструватися')
    #     register(message)
    # else:
    bot.send_message(chat_id=message.from_user.id,
                     text='Вибери пункт меню:',
                     reply_markup=make_menu_keyboard(message))


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in menu_buttons)
def get_student_messages(message):
    if message.text == menu_buttons[0]:
        search_aud(message)
    elif message.text == menu_buttons[1]:
        bot.send_message(chat_id=message.from_user.id,
                         text=('1 пара  |  08:30  |  09:50\n'
                               '2 пара  |  10:05  |  11:25\n'
                               '3 пара  |  11:55  |  13:15\n'
                               '4 пара  |  13:25  |  14:45\n'
                               '5 пара  |  14:55  |  16:15\n'
                               '6 пара  |  16:45  |  18:05\n'
                               '7 пара  |  18:15  |  19:35\n'
                               '8 пара  |  19:45  |  21:05\n'))
    elif message.text == menu_buttons[2]:
        teachers_schelude(message)
    elif message.text == menu_buttons[3]:
        get_events_schelude(message)
    elif message.text == menu_buttons[4]:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='http://www.zntu.edu.ua', url='http://www.zntu.edu.ua'))
        bot.send_message(chat_id=message.chat.id, text='Сайт НУЗП', reply_markup=markup)
    elif message.text == menu_buttons[5]:
        show_studdekan_keyboard(message)
    elif message.text == menu_buttons[6]:
        show_headman_keyboard(message)
    elif message.text == menu_buttons[7]:
        show_dekanat_keyboard(message)
    elif message.text == menu_buttons[8]:
        start_message(message)


@restricted_studdekan
def show_studdekan_keyboard(message):
    bot.send_message(chat_id=message.from_user.id, text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(studdekan_buttons))


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
    bot.send_message(chat_id=message.from_user.id, text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(headman_buttons))


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in headman_buttons)
@restricted_headman
def get_headman_messages(message):
    if message.text == headman_buttons[0]:
        print('1')
    elif message.text == headman_buttons[1]:
        print('2')
    elif message.text == headman_buttons[2]:
        start_message(message)


def show_dekanat_keyboard(message):
    bot.send_message(chat_id=message.from_user.id, text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(dekanat_buttons))


def make_d():
    return make_role_replykeyboard(dekanat_buttons)


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in dekanat_buttons)
def get_dekanat_messages(message):
    if message.text == dekanat_buttons[0]:
        rate_headman(message)
    elif message.text == dekanat_buttons[1]:
        remind_journal(message)
    elif message.text == dekanat_buttons[2]:
        send_file(message)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(chat_id=message.from_user.id, text="я не знаю как тебе помочь")


# SERVICE COMMANDS
@bot.message_handler(commands=['fill'])
@restricted_studdekan
def add_all(message):
    Group.add_groups()
    Student.add_students()
    Event.add_events()
    Event.add_visitors()


@bot.message_handler(commands=['del'])
@restricted_studdekan
def delete_all(message):
    db.delete()


@bot.message_handler(content_types=['text',
                                    'audio',
                                    'document',
                                    'photo',
                                    'sticker',
                                    'video',
                                    'video_note',
                                    'voice',
                                    'location',
                                    'contact',
                                    'new_chat_members',
                                    'left_chat_member',
                                    'new_chat_title',
                                    'new_chat_photo',
                                    'delete_chat_photo',
                                    'group_chat_created',
                                    'supergroup_chat_created',
                                    'channel_chat_created',
                                    'migrate_to_chat_id',
                                    'migrate_from_chat_id',
                                    'pinned_message'])
def get_text_messages(message):
    bot.send_message(chat_id=message.from_user.id, text="Отвали или обратись за помощью /help.")







