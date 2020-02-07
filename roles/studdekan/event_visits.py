from flask import Blueprint
from credentials import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard import make_keyboard
from db.group import Group
from db.event import Event
from db.student import Student
from helpers import restricted_studdekan, get_fio, make_event_visitors_table, make_student_events_table
import xlsxwriter
from emoji import emojize
import time

event_visits = Blueprint('event_visits', __name__)


@event_visits.route('/event_visits')
def event_visits_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Учасники заходу {emojize(":page_facing_up:", use_aliases=True)}',
                                      callback_data='event_visitors'))
    keyboard.add(InlineKeyboardButton(text=f'Відвідування заходів {emojize(":bar_chart:", use_aliases=True)}',
                                      callback_data='student_events'))

    bot.send_message(chat_id=message.from_user.id, text='Вибери дію:', reply_markup=keyboard)


@bot.message_handler(commands=['stud'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('student_events'))
@restricted_studdekan
def get_student_events(call):
    file_name = prepare_student_events_table()
    doc = open(f'./tmp/{file_name}.xlsx', 'rb')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Документ з відвідуваннями заходів:')
    bot.send_document(chat_id=call.from_user.id, data=doc)


def prepare_student_events_table():
    file_name = 'Відвідування заходів'
    workbook = xlsxwriter.Workbook(f'./tmp/{file_name}.xlsx')

    for group in Group.get_groups()[:4]:
        students = Event.get_visitor_students(group.name)

        stud_dict = {}

        for student in students:
            s_name = get_fio(Student.get_student_by_id(student[1].student_id).name)
            s_event = Event.get_event(student[1].event_id).name

            stud_dict.setdefault(s_name, []).append(s_event)

        worksheet = workbook.add_worksheet(name=f'КНТ-{group.name}')
        make_student_events_table(stud_dict, group.name, worksheet, workbook)

    workbook.close()
    return file_name


# table of participants
@bot.message_handler(commands=['visits'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('event_visitors'))
@restricted_studdekan
def get_event_visitors(call):
    Event.add_events()

    event_keyboard = make_keyboard(keyboard_type='event',
                                   elem_list=Event.get_all_events(),
                                   marker='eventvisitor_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Учасники якого заходу?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('eventvisitor_') == True)
def get_event_visitors_callback(call):
    event_id = call.data.split('_')[1]
    Event.add_visitors(event_id)

    prepare_event_visitors_table(event_id)
    doc = open(f'./tmp/{Event.get_event(event_id).name}.xlsx', 'rb')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Документ з учасниками:')
    bot.send_document(chat_id=call.from_user.id, data=doc)


def prepare_event_visitors_table(event_id):
    visitor_ids = Event.get_visitors(event_id)
    stud_dict = {}

    for visitor_id in visitor_ids:
        student = Student.get_student_by_id(visitor_id)

        s_name = get_fio(student.name)
        s_group = f'КНТ-{Group.get_group_by_id(student.group_id)}'

        stud_dict.setdefault(s_group, []).append(s_name)

    event_name = Event.get_event(event_id).name

    workbook = xlsxwriter.Workbook(f'./tmp/{event_name}.xlsx')
    worksheet = workbook.add_worksheet(name=event_name)

    make_event_visitors_table(stud_dict, worksheet, workbook)
    workbook.close()
