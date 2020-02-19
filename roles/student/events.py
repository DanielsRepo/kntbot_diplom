from flask import Blueprint
from credentials import *
from db.event import Event
from keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

events = Blueprint('events', __name__)


@events.route('/events')
# get_events_schelude
def get_events_schelude(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keys_list = []

    for event in Event.get_all_events():
        keys_list.append(InlineKeyboardButton(text=event.name, callback_data=f'schelude_{event.id}'))
        keys_list.append(InlineKeyboardButton(text=str(event.date), callback_data=f'schelude_{event.id}'))

    keyboard.add(*keys_list)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'{emojize(":man_juggling:", use_aliases=True)} Розклад заходів '
                          f'{emojize(":performing_arts:", use_aliases=True)}',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('schelude_'))
def get_events_schelude_callback(call):
    event_id = call.data.split('_')[1]
    event = Event.get_event(event_id)

    message = f'{event.name} {event.place} {event.date} {event.time}'

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=f'{emojize(":pencil2:", use_aliases=True)} Зареєструватися',
                                      callback_data=f'regon_{event.id}'))

    bot.send_message(call.from_user.id, text=message, reply_markup=keyboard)


# registration
@bot.callback_query_handler(func=lambda call: call.data.startswith('regon_'))
def register_on_event_callback(call):
    event_id = call.data.split('_')[1]

    Event.add_visitor(event_id, call.from_user.id)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Реєстрація пройшла успішно {emojize(":white_check_mark:", use_aliases=True)}')
