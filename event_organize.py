from flask import Blueprint
from credentials import *
from db.event import Event
from db.student import Student
from db.group import Group
from keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers import restricted
import xlsxwriter
import time

event_organize = Blueprint('event_organize', __name__)


@event_organize.route('/event_organize')
def get_fio(s):
    return f"{s.split(' ')[0]} {s.split(' ')[1][0]}. {s.split(' ')[2][0]}."
    # res = []
    # for s in students:
    #     try:
    #         s = f"{s.split(' ')[0]} {s.split(' ')[1][0]}. {s.split(' ')[2][0]}."
    #         res.append(s)
    #     except IndexError:
    #         continue
    #
    # return res


def doit(stud_dict, worksheet, workbook):
    col_counter = 0

    for group, students in stud_dict.items():
        col = col_counter

        cell_format = workbook.add_format({'bold': True, 'align': 'center'})
        worksheet.write(0, col, group, cell_format)

        col_width = max([len(s) for s in students])

        stud_list = stud_dict[group]

        for i in range(len(stud_list)):
            worksheet.set_column(i + 1, col, col_width)
            worksheet.write(i + 1, col, stud_list[i])

        col_counter += 1


@bot.message_handler(commands=['exc'])
def excel(message):
    # Event.add_visitors()
    visitor_ids = Event.get_visitors(1)
    stud_dict = {}

    for visitor_id in visitor_ids:
        if visitor_id != 374464076:
            s = Student.get_student_by_id(visitor_id)

            s_name = get_fio(s.name)
            s_group = f'КНТ-{Group.get_group_by_id(s.group_id)}'

            if s_group in stud_dict:
                stud_dict[s_group].append(s_name)
            else:
                stud_dict[s_group] = [s_name]

    workbook = xlsxwriter.Workbook('EVENT.xlsx')
    worksheet = workbook.add_worksheet()
    doit(stud_dict, worksheet, workbook)
    workbook.close()

    bot.send_message(message.from_user.id, text='added')


def events_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='Создать мероприятие', callback_data='new_event'))
    keyboard.add(InlineKeyboardButton(text='Удалить мероприятие', callback_data='delete_event'))
    keyboard.add(InlineKeyboardButton(text='Изменить мероприятие', callback_data='change_event'))
    keyboard.add(InlineKeyboardButton(text='Обьявить мероприятие', callback_data='alarm_event'))

    bot.send_message(message.from_user.id, text='Выбери', reply_markup=keyboard)


# creating
@bot.message_handler(commands=['org'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('new_event'))
@restricted
def create_event(message):
    message = bot.send_message(message.from_user.id, "Название мероприятия")
    bot.register_next_step_handler(message, name_event)


def name_event(message):
    name = message.text
    event = Event.add_event(name=name)
    message = bot.send_message(message.from_user.id, "Место проведения")
    bot.register_next_step_handler(message, place_event, event.id)


def place_event(message, event_id):
    Event.update_event(event_id=event_id, place=message.text)

    message = bot.send_message(message.from_user.id, "Дата проведения")
    bot.register_next_step_handler(message, date_event, event_id)


def date_event(message, event_id):
    Event.update_event(event_id=event_id, date=message.text)

    message = bot.send_message(message.from_user.id, "Время проведения")
    bot.register_next_step_handler(message, time_event, event_id)


def time_event(message, event_id):
    Event.update_event(event_id=event_id, time=message.text)
    message = bot.send_message(message.from_user.id, "Баннер мероприятия")
    bot.register_next_step_handler(message, picture_event, event_id)


@bot.message_handler(content_types=['photo'])
def picture_event(message, event_id):
    file_id = message.photo[-1].file_id

    Event.update_event(event_id=event_id, poster=file_id)

    event = Event.get_event(event_id)

    success_message = f'''
        Организация мероприятия {event.name}
        в {event.place} {event.date} {event.time}
        на удивление прошла успешно
    '''
    bot.send_photo(message.from_user.id, photo=file_id, caption=success_message)


# deleting
@bot.message_handler(commands=['edel'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_event'))
@restricted
def delete_event(message):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'edel_')

    bot.send_message(message.from_user.id, text='Какое мероприятие удалить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edel_') == True)
def del_event_callback(call):
    event_id = call.data.split('_')[1]
    bot.send_message(call.from_user.id, text=f'Мероприятие {Event.get_event(event_id).name} удалено')
    Event.delete_event(event_id)


# changing
@bot.message_handler(commands=['ech'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('change_event'))
@restricted
def change_event(message):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'ech_')

    bot.send_message(message.from_user.id, text='Какое мероприятие изменить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ech_') == True)
def event_callback(call):
    event_id = call.data.split('_')[1]
    event_name = Event.get_event(event_id).name

    change_event_keyboard = InlineKeyboardMarkup()
    change_event_keyboard.add(InlineKeyboardButton(text='Название', callback_data='name_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Место проведения', callback_data='place_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Дата проведения', callback_data='date_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Время проведения', callback_data='time_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Постер', callback_data='poster_' + event_id))

    bot.send_message(call.from_user.id, text=f'Что нужно изменить в мероприятии {event_name} ?',
                     reply_markup=change_event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('name_') or call.data.startswith('place_') or
                    call.data.startswith('date_') or call.data.startswith('time_') or call.data.startswith('poster_'))
def change_event_callback(call):
    event_id = call.data.split('_')[1]

    if call.data.startswith('name_'):
        message = bot.send_message(call.from_user.id, "Новое имя")
        bot.register_next_step_handler(message, change_event_name, event_id)
    elif call.data.startswith('place_'):
        message = bot.send_message(call.from_user.id, "Новое место")
        bot.register_next_step_handler(message, change_event_place, event_id)
    elif call.data.startswith('date_'):
        message = bot.send_message(call.from_user.id, "Новая дата")
        bot.register_next_step_handler(message, change_event_date, event_id)
    elif call.data.startswith('time_'):
        message = bot.send_message(call.from_user.id, "Новое время")
        bot.register_next_step_handler(message, change_event_time, event_id)
    elif call.data.startswith('poster_'):
        message = bot.send_message(call.from_user.id, "Новый постер")
        bot.register_next_step_handler(message, change_event_poster, event_id)


def change_event_name(message, event_id):
    Event.update_event(event_id, name=message.text)

    event = Event.get_event(event_id)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_message(message.from_user.id, text=success_message)


def change_event_place(message, event_id):
    Event.update_event(event_id, place=message.text)

    event = Event.get_event(event_id)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_message(message.from_user.id, text=success_message)


def change_event_date(message, event_id):
    Event.update_event(event_id, date=message.text)

    event = Event.get_event(event_id)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_message(message.from_user.id, text=success_message)


def change_event_time(message, event_id):
    Event.update_event(event_id, time=message.text)

    event = Event.get_event(event_id)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_message(message.from_user.id, text=success_message)


def change_event_poster(message, event_id):
    file_id = message.photo[-1].file_id
    Event.update_event(event_id, poster=file_id)

    event = Event.get_event(event_id)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_photo(message.from_user.id, photo=file_id, caption=success_message)


# notification
@bot.message_handler(commands=['alarm'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('alarm_event'))
@restricted
def notification(message):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'alarm_')

    bot.send_message(message.from_user.id, text='Какое мероприятие высветить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('alarm_') == True)
def notification_callback(call):
    event_id = call.data.split('_')[1]
    event = Event.get_event(event_id)

    message = f'''
        {event.place} {event.time} будет {event.name}
    '''
    channel_id = '-1001104545927'
    bot.send_photo(channel_id, photo=event.poster, caption=message)


@bot.message_handler(commands=['sch'])
def schelude(message):
    Event.add_events()

    keyboard = InlineKeyboardMarkup(row_width=2)
    keys_list = []

    for event in Event.get_all_events():
        keys_list.append(InlineKeyboardButton(text=event.name, callback_data=f'schelude_{event.id}'))
        keys_list.append(InlineKeyboardButton(text=str(event.date), callback_data=f'schelude_{event.id}'))

    keyboard.add(*keys_list)

    bot.send_message(message.from_user.id, text=f'Расписание мероприятий', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('schelude_') == True)
def schelude_callback(call):
    event_id = call.data.split('_')[1]
    event = Event.get_event(event_id)

    message = f'''
        {event.name} {event.place} {event.date} {event.time}
    '''

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Зарегистрироваться', callback_data=f'regon_{event.id}'))

    bot.send_message(call.from_user.id, text=message, reply_markup=keyboard)
    # bot.send_photo(channel_id, photo=event.poster, caption=message)


# registration
@bot.message_handler(commands=['regon'])
def register_on_event(message):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'regon_')

    bot.send_message(message.from_user.id, text='На какое мероприятие идешь?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('regon_'))
def register_on_event_callback(call):
    event_id = call.data.split('_')[1]
    event_name = Event.get_event(event_id).name

    student = Student.get_student_by_id(call.from_user.id)

    Event.add_visitor(event_id, call.from_user.id)
    bot.send_message(call.from_user.id, text=f'Ты {student.name} на мероприятие {event_name} зарегистрирован')



# scheduler = schedule.Scheduler()
#     def my_job(message):
#         bot.send_message(message.from_user.id, text='ЗАПОЛНИТЬ ЖУРНАЛЫ')

    # scheduler.every(1).seconds.do(my_job, message=message)

#     while True:
#         scheduler.run_pending()
#         time.sleep(1)
#
#
# @bot.message_handler(commands=['stop'])
# def stop(message):
#     scheduler.jobs.clear()
