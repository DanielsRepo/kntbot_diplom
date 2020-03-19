from flask import Blueprint
from keyboards.keyboard import make_menu_keyboard, menu_buttons, make_role_replykeyboard, \
    studdekan_buttons, teacher_buttons, dekanat_buttons

from database.database import db
from database.group import Group
from database.student import Student
from database.event import Event
from database.subject import Subject
from database.cathedra import Cathedra
from database.teacher import Teacher

from roles.student.auditory_search import search_aud
from roles.student.teachers import teacher_keyboard
from roles.student.studying import studying_keyboard
from roles.student.univer_info import univer_info_keyboard
from roles.student.events_schelude import get_events_schelude
from roles.student.registration import register, add_another_fac

from roles.studdekan.headman_management import headman_keyboard
from roles.studdekan.profcomdebtor_management import debtor_keyboard
from roles.studdekan.event_organization import event_organize_keyboard
from roles.studdekan.getting_eventvisits import event_visits_keyboard

from roles.dekanat.headman_communication import rate_headman, remind_journal, send_message_or_file
from roles.dekanat.rating_formation import create_rating

from roles.teacher.grade_assignment import assign_grade
from roles.teacher.subjectdebtor_management import subject_debtor_keyboard
from roles.teacher.sending_methods import send_message_or_file

from credentials import bot
from helpers.role_helper import restricted_studdekan, restricted_dekanat, restricted_teacher, \
    LIST_OF_DEKANAT, LIST_OF_ADMINS, LIST_OF_TEACHERS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

menu = Blueprint('menu', __name__)


@menu.route('/menu')
@bot.message_handler(commands=['start', 'cancel'])
def start_message(message):
    add_all(message)

    chat_id = message.from_user.id

    if chat_id in LIST_OF_ADMINS:
        bot.send_message(chat_id=chat_id,
                         text='Вибери пункт меню:',
                         reply_markup=make_menu_keyboard(message, other_fac=False))
    elif chat_id in LIST_OF_DEKANAT or LIST_OF_TEACHERS:
        bot.send_message(chat_id=chat_id,
                         text='Виберіть пункт меню:',
                         reply_markup=make_menu_keyboard(message, other_fac=False))
    elif Student.get_student_by_id(chat_id) is None:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton(text='Так', callback_data='yes'),
            InlineKeyboardButton(text='Ні', callback_data='no')
        )

        bot.send_message(chat_id=chat_id,
                         text=f'Привіт {emojize(":wave:", use_aliases=True)}\nТи з ФКНТ?',
                         reply_markup=keyboard)
    elif Student.check_fac(chat_id):
        bot.send_message(chat_id=chat_id,
                         text='Вибери пункт меню:',
                         reply_markup=make_menu_keyboard(message, other_fac=False))
    elif not Student.check_fac(chat_id):
        bot.send_message(chat_id=chat_id,
                         text='Вибери пункт меню:',
                         reply_markup=make_menu_keyboard(message, other_fac=True))


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def knt_or_not(call):
    if call.data == 'yes':
        bot.send_message(chat_id=call.from_user.id,
                         text='Для користування ботом треба зареєструватися')
        register(call)
    elif call.data == 'no':
        add_another_fac(call)
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        bot.send_message(chat_id=call.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_menu_keyboard(call, other_fac=True))


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
        bot.send_message(chat_id=374464076, text='#asked_bells')
    elif message.text == menu_buttons[2]:
        studying_keyboard(message)
    elif message.text == menu_buttons[3]:
        teacher_keyboard(message)
    elif message.text == menu_buttons[4]:
        get_events_schelude(message)
    elif message.text == menu_buttons[5]:
        univer_info_keyboard(message)
    elif message.text == menu_buttons[6]:
        show_studdekan_keyboard(message)
    elif message.text == menu_buttons[7]:
        show_dekanat_keyboard(message)
    elif message.text == menu_buttons[8]:
        show_teacher_keyboard(message)
    elif message.text == menu_buttons[9]:
        start_message(message)


@restricted_studdekan
def show_studdekan_keyboard(message):
    bot.send_message(chat_id=message.from_user.id, text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(studdekan_buttons))


def show_dekanat_keyboard(message):
    bot.send_message(chat_id=message.from_user.id, text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(dekanat_buttons))


@restricted_teacher
def show_teacher_keyboard(message):
    bot.send_message(chat_id=message.from_user.id, text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(teacher_buttons))


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


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in dekanat_buttons)
@restricted_dekanat
def get_dekanat_messages(message):
    if message.text == dekanat_buttons[0]:
        rate_headman(message)
    elif message.text == dekanat_buttons[1]:
        remind_journal(message)
    elif message.text == dekanat_buttons[2]:
        send_message_or_file(message)
    elif message.text == dekanat_buttons[3]:
        create_rating(message)


@bot.message_handler(func=lambda message: message.content_type == 'text' and message.text in teacher_buttons)
@restricted_teacher
def get_teacher_messages(message):
    if message.text == teacher_buttons[0]:
        assign_grade(message)
    elif message.text == teacher_buttons[1]:
        subject_debtor_keyboard(message)
    elif message.text == teacher_buttons[2]:
        send_message_or_file(message)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(chat_id=message.from_user.id,
                     text="Доступні команди:\n\n"
                          "/start - почати роботу з ботом\n"
                          "/cancel - відміна дії\n"
                          "/help - допомога")
    bot.send_message(chat_id=374464076, text="#askedhelp")


@bot.message_handler(commands=['fill'])
def add_all(message):
    Group.add_groups()
    Student.add_students()
    Event.add_events()
    Event.add_visitors()

    Cathedra.add_cathedras()
    Teacher.add_teachers()

    Subject.add_subjects()


@bot.message_handler(commands=['del'])
@restricted_studdekan
def delete_all(message):
    db.delete()
    bot.send_message(chat_id=message.from_user.id, text="database is cleared")


@bot.message_handler(commands=['groups301198'])
@restricted_studdekan
def add_groups(message):
    Group.add_groups()
    bot.send_message(chat_id=message.from_user.id, text="groups added")


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
def get_trash_messages(message):
    help_message(message)
