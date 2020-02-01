from flask import Blueprint
from credentials import *
from db.event import Event
from db.student import Student
from keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

events = Blueprint('events', __name__)


@events.route('/events')
# get_events_schelude
@bot.message_handler(commands=['sch'])
def get_events_schelude(message):
    Event.add_events()

    keyboard = InlineKeyboardMarkup(row_width=2)
    keys_list = []

    for event in Event.get_all_events():
        keys_list.append(InlineKeyboardButton(text=event.name, callback_data=f'schelude_{event.id}'))
        keys_list.append(InlineKeyboardButton(text=str(event.date), callback_data=f'schelude_{event.id}'))

    keyboard.add(*keys_list)

    bot.send_message(message.from_user.id, text=f'Розклад заходів', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('schelude_') == True)
def get_events_schelude_callback(call):
    event_id = call.data.split('_')[1]
    event = Event.get_event(event_id)

    message = f'''
        {event.name} {event.place} {event.date} {event.time}
    '''

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Зареєструватися', callback_data=f'regon_{event.id}'))

    bot.send_message(call.from_user.id, text=message, reply_markup=keyboard)


# registration
@bot.message_handler(commands=['regon'])
def register_on_event(message):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'regon_')

    bot.send_message(message.from_user.id, text='На какое мероприятие идешь?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('regon_'))
def register_on_event_callback(call):
    event_id = call.data.split('_')[1]

    Event.add_visitor(event_id, call.from_user.id)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Реєстрація пройшла успішно')