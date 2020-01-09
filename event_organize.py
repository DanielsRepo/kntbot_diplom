from flask import Blueprint
from credentials import *
from db.event import Event
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

event_organize = Blueprint('event_organize', __name__)


@event_organize.route('/event_organize')
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


@bot.message_handler(commands=['edel'])
def delete_event(message):
    event_keyboard = InlineKeyboardMarkup()
    for event in Event.get_all_events():
        event_keyboard.add(InlineKeyboardButton(text=event.name, callback_data=event.id))

    bot.send_message(message.from_user.id, text='Какое мероприятие удалить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def event_callback_worker(call):
    bot.send_message(call.from_user.id, text=f'Мероприятие {Event.get_event(call.data).name} удалено')
    Event.delete_event(call.data)

