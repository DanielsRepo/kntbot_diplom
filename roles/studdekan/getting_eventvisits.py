from flask import Blueprint
from credentials import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.keyboard import make_keyboard
from database.group import Group
from database.event import Event
from database.event_visitor import EventVisitor
from database.student import Student
from helpers.xlsx_helper import get_fio, make_event_visitors_table, make_student_events_table
from helpers.role_helper import restricted_studdekan
from emoji import emojize
import os

event_visits = Blueprint('event_visits', __name__)


@event_visits.route('/event_visits')
def event_visits_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Учасники заходу {emojize(":page_facing_up:", use_aliases=True)}',
                                      callback_data='event_visitors'))
    keyboard.add(InlineKeyboardButton(text=f'Відвідування заходів {emojize(":bar_chart:", use_aliases=True)}',
                                      callback_data='student_events'))

    bot.send_message(chat_id=message.from_user.id, text='Вибери дію:', reply_markup=keyboard)


# table of event's participants
@bot.callback_query_handler(func=lambda call: call.data.startswith('event_visitors'))
@restricted_studdekan
def get_event_visitors(call):
    event_keyboard = make_keyboard(keyboard_type='event',
                                   elem_list=Event.get_all_events(),
                                   marker='eventvisitor_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Учасники якого заходу?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('eventvisitor_'))
def send_event_visitors_file(call):
    event_id = call.data.split('_')[1]
    event_name = Event.get_event(event_id).name

    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tmp/'

    stud_dict, otherfac_list = prepare_event_visitors_table(event_id)
    make_event_visitors_table(visitors_dict=stud_dict, otherfac_list=otherfac_list, event_name=event_name, file_path=file_path)

    doc = open(f'{file_path}{event_name}.xlsx', 'rb')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Документ з учасниками:')
    bot.send_document(chat_id=call.from_user.id, data=doc)


def prepare_event_visitors_table(event_id):
    visitor_ids = EventVisitor.get_visitors(event_id)
    stud_dict = {}
    otherfac_list = []

    for visitor_id in visitor_ids:
        student = Student.get_student_by_id(visitor_id)

        if Group.get_group_by_id(student.group_id) == 'other':
            otherfac_list.append(EventVisitor.get_visitor_by_id(visitor_id).note)
        else:
            try:
                s_name = get_fio(student.name)
                s_group = f'КНТ-{Group.get_group_by_id(student.group_id)}'

                stud_dict.setdefault(s_group, []).append(s_name)
            except AttributeError:
                continue

    return stud_dict, otherfac_list


# table of group's visitors
@bot.callback_query_handler(func=lambda call: call.data.startswith('student_events'))
@restricted_studdekan
def send_student_events_file(call):
    file_name = 'Відвідування заходів'
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tmp/'

    group_dict = prepare_student_events_table()
    make_student_events_table(group_dict=group_dict, file_name=file_name, file_path=file_path)

    doc = open(f'{file_path}{file_name}.xlsx', 'rb')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Документ з відвідуваннями заходів:')
    bot.send_document(chat_id=call.from_user.id, data=doc)


def prepare_student_events_table():
    group_dict = {}

    for group in Group.get_groups():
        students = EventVisitor.get_visitor_students(group.id)
        if not students:
            continue
        else:
            stud_dict = {}

            for student in students:
                try:
                    s_name = get_fio(Student.get_student_by_id(student[1].student_id).name)
                    s_event = Event.get_event(student[1].event_id).name

                    stud_dict.setdefault(s_name, []).append(s_event)
                except AttributeError:
                    continue

        group_dict[group.name] = stud_dict

    return group_dict
