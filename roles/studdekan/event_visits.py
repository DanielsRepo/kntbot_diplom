from flask import Blueprint
from credentials import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard import make_keyboard
from db.group import Group
from db.event import Event
from db.student import Student
from helpers import restricted_studdekan, get_fio, make_event_visitors_table, make_student_events_table
import xlsxwriter

event_visits = Blueprint('event_visits', __name__)


@event_visits.route('/event_visits')
def event_visits_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='Учасники мероприятия', callback_data='event_visitors'))
    keyboard.add(InlineKeyboardButton(text='Студенты и их посещения', callback_data='student_events'))

    bot.send_message(message.from_user.id, text='Выбери', reply_markup=keyboard)


@bot.message_handler(commands=['stud'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('student_events'))
@restricted_studdekan
def get_student_events(call):
    prepare_student_events_table(call)
    doc = open(f'./tmp/STUD.xlsx', 'rb')
    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Документ:')
    bot.send_document(call.from_user.id, doc)


def prepare_student_events_table(call):
    workbook = xlsxwriter.Workbook(f'./tmp/STUD.xlsx')

    for group in Group.get_groups()[:4]:
        students = Event.get_visitor_students(group.name)

        stud_dict = {}

        for i in students:
            s = Student.get_student_by_id(i[1].student_id)

            s_name = get_fio(s.name)
            s_event = Event.get_event(i[1].event_id).name

            if s_name in stud_dict:
                stud_dict[s_name].append(s_event)
            else:
                stud_dict[s_name] = [s_event]

        worksheet = workbook.add_worksheet(name=f'КНТ-{group.name}')
        make_student_events_table(stud_dict, group.name, worksheet, workbook)

    workbook.close()


# table of participants
@bot.message_handler(commands=['visits'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('event_visitors'))
@restricted_studdekan
def get_event_visitors(call):
    Event.add_events()

    event_keyboard = make_keyboard('event', Event.get_all_events(), 'eventvisitor_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Учасники какого мероприятия?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('eventvisitor_') == True)
def get_event_visitors_callback(call):
    event_id = call.data.split('_')[1]
    Event.add_visitors(event_id)

    prepare_event_visitors_table(event_id)

    doc = open(f'./tmp/{Event.get_event(event_id).name}.xlsx', 'rb')
    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Документ с учасниками:')
    bot.send_document(call.from_user.id, doc)


def prepare_event_visitors_table(event_id):
    visitor_ids = Event.get_visitors(event_id)
    stud_dict = {}

    for visitor_id in visitor_ids:
        s = Student.get_student_by_id(visitor_id)

        s_name = get_fio(s.name)
        s_group = f'КНТ-{Group.get_group_by_id(s.group_id)}' # временно

        if s_group in stud_dict:
            stud_dict[s_group].append(s_name)
        else:
            stud_dict[s_group] = [s_name]

    workbook = xlsxwriter.Workbook(f'./tmp/{Event.get_event(event_id).name}.xlsx')
    worksheet = workbook.add_worksheet(name=Event.get_event(event_id).name)

    make_event_visitors_table(stud_dict, worksheet, workbook)
    workbook.close()


