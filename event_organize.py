from flask import Blueprint
from credentials import *
from db.event import Event
from db.student import Student
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Poll, PollOption
import schedule
import time

event_organize = Blueprint('event_organize', __name__)


@event_organize.route('/event_organize')
# creating
@bot.message_handler(commands=['org'])
def create_event(message):
    message = bot.send_message(message.from_user.id, "Название мероприятия")
    bot.register_next_step_handler(message, name_event)


def name_event(message):
    name = message.text
    event = Event.add_event(name=name)
    message = bot.send_message(message.from_user.id, "Место проведения")
    bot.register_next_step_handler(message, place_event, event.id)


def place_event(message, event_id):
    Event.update_event(id=event_id, place=message.text)

    message = bot.send_message(message.from_user.id, "Время проведения")
    bot.register_next_step_handler(message, time_event, event_id)


def time_event(message, event_id):
    Event.update_event(id=event_id, time=message.text)
    message = bot.send_message(message.from_user.id, "Баннер мероприятия")
    bot.register_next_step_handler(message, picture_event, event_id)


@bot.message_handler(content_types=['photo'])
def picture_event(message, event_id):
    file_id = message.photo[-1].file_id

    Event.update_event(id=event_id, poster=file_id)

    event = Event.get_event(event_id)

    success_message = f'''
        Организация мероприятия {event.name}
        в {event.place}
        на {event.time}
        на удивление прошла успешно
    '''
    bot.send_photo(message.from_user.id, photo=file_id, caption=success_message)


# deleting
@bot.message_handler(commands=['edel'])
def delete_event(message):
    event_keyboard = InlineKeyboardMarkup()
    for event in Event.get_all_events():
        event_keyboard.add(InlineKeyboardButton(text=event.name, callback_data='edel_' + event.name))

    bot.send_message(message.from_user.id, text='Какое мероприятие удалить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('edel_') == True)
def del_event_callback(call):
    event_name = call.data.split('_')[1]
    bot.send_message(call.from_user.id, text=f'Мероприятие {event_name} удалено')
    Event.delete_event(Event.get_id_by_name(event_name))


# changing
@bot.message_handler(commands=['ech'])
def change_event(message):
    event_keyboard = InlineKeyboardMarkup()
    for event in Event.get_all_events():
        event_keyboard.add(InlineKeyboardButton(text=event.name, callback_data='ech_' + event.name))

    bot.send_message(message.from_user.id, text='Какое мероприятие изменить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('ech_') == True)
def event_callback(call):
    event_name = call.data.split('_')[1]
    event_id = str(Event.get_id_by_name(event_name))

    change_event_keyboard = InlineKeyboardMarkup()
    change_event_keyboard.add(InlineKeyboardButton(text='Название', callback_data='name_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Место проведения', callback_data='place_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Время проведения', callback_data='time_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Постер', callback_data='poster_' + event_id))

    bot.send_message(call.from_user.id, text=f'Что нужно изменить в мероприятии {event_name} ?',
                     reply_markup=change_event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('name_') or call.data.startswith('place_') or
                                              call.data.startswith('time_') or call.data.startswith('poster_'))
def change_event_callback(call):
    event_id = call.data.split('_')[1]

    if call.data.startswith('name_'):
        message = bot.send_message(call.from_user.id, "Новое имя")
        bot.register_next_step_handler(message, change_event_name, event_id)
    elif call.data.startswith('place_'):
        message = bot.send_message(call.from_user.id, "Новое место")
        bot.register_next_step_handler(message, change_event_place, event_id)
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


# registration
@bot.message_handler(commands=['regon'])
def register_on_event(message):
    event_keyboard = InlineKeyboardMarkup()
    for event in Event.get_all_events():
        event_keyboard.add(InlineKeyboardButton(text=event.name, callback_data='regon_' + event.name))

    bot.send_message(message.from_user.id, text='На какое мероприятие идешь?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('regon_'))
def register_on_event_callback(call):
    event_name = call.data.split('_')[1]
    event_id = Event.get_id_by_name(event_name)

    student = Student.get_user(call.from_user.id)

    Event.add_visitor(event_id, call.from_user.id)
    bot.send_message(call.from_user.id, text=f'Ты {student.name} на мероприятие {event_name} зарегистрирован')


@bot.message_handler(commands=['poll'])
def create_poll(message):
    message = bot.send_message(message.from_user.id, text='Вопрос опроса')
    bot.register_next_step_handler(message, add_poll_options)


def add_poll_options(message):
    poll = Poll(message.text)

    message = bot.send_message(message.from_user.id, text='Пункты опроса')
    bot.register_next_step_handler(message, send_poll, poll)


def send_poll(message, poll):
    options = message.text.split('\n')
    for i in options:
        poll.add(PollOption(i))

    channel_id = '-1001104545927'
    bot.send_poll(channel_id, poll)


scheduler = schedule.Scheduler()


@bot.message_handler(commands=['alarm'])
def notification(message):
    event_keyboard = InlineKeyboardMarkup()
    for event in Event.get_all_events():
        event_keyboard.add(InlineKeyboardButton(text=event.name, callback_data='alarm_' + event.name))

    bot.send_message(message.from_user.id, text='Какое мероприятие высветить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('alarm_') == True)
def notification_callback(call):
    event = Event.get_event(Event.get_id_by_name(call.data.split('_')[1]))

    message = f'''
        {event.place} {event.time} будет {event.name}
    '''
    channel_id = '-1001104545927'
    bot.send_photo(channel_id, photo=event.poster, caption=message)


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
