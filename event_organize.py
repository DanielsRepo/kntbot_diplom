from flask import Blueprint
from credentials import *
from db.event import Event
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


event_organize = Blueprint('event_organize', __name__)


@event_organize.route('/event_organize', methods=['GET', 'POST'])
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
    # message = bot.send_message(message.from_user.id, "Баннер мероприятия")
    # bot.register_next_step_handler(message, picture_event, event_id)


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
        event_keyboard.add(InlineKeyboardButton(text=event.name, callback_data='del ' + event.name))

    bot.send_message(message.from_user.id, text='Какое мероприятие удалить?', reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['del ' + event.name for event in Event.get_all_events()])
def del_event_callback(call):
    event_name = call.data[4:]
    bot.send_message(call.from_user.id, text=f'Мероприятие {event_name} удалено')
    Event.delete_event(Event.get_id_by_name(event_name))


@bot.message_handler(commands=['ech'])
def change_event(message):
    event_keyboard = InlineKeyboardMarkup()
    for event in Event.get_all_events():
        event_keyboard.add(InlineKeyboardButton(text=event.name, callback_data='ech ' + event.name))

    bot.send_message(message.from_user.id, text='Какое мероприятие изменить?', reply_markup=event_keyboard)


EVENT_ID = 0


@bot.callback_query_handler(func=lambda call: call.data in ['ech ' + event.name for event in Event.get_all_events()])
def event_callback(call):
    global EVENT_ID
    event_name = call.data[4:]
    EVENT_ID = Event.get_id_by_name(event_name)

    change_event_keyboard = InlineKeyboardMarkup()
    change_event_keyboard.add(InlineKeyboardButton(text='Название', callback_data='name'))
    change_event_keyboard.add(InlineKeyboardButton(text='Место проведения', callback_data='place'))
    change_event_keyboard.add(InlineKeyboardButton(text='Время проведения', callback_data='time'))
    change_event_keyboard.add(InlineKeyboardButton(text='Постер', callback_data='poster'))

    bot.send_message(call.from_user.id, text=f'Что нужно изменить в мероприятии {event_name} ?', reply_markup=change_event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['name', 'place', 'time', 'poster'])
def change_event_callback(call):
    if call.data == 'name':
        message = bot.send_message(call.from_user.id, "Новое имя")
        bot.register_next_step_handler(message, change_event_name)
    elif call.data == 'place':
        message = bot.send_message(call.from_user.id, "Новое место")
        bot.register_next_step_handler(message, change_event_place)
    elif call.data == 'time':
        message = bot.send_message(call.from_user.id, "Новое время")
        bot.register_next_step_handler(message, change_event_time)
    elif call.data == 'poster':
        message = bot.send_message(call.from_user.id, "Новый постер")
        bot.register_next_step_handler(message, change_event_poster)


def change_event_name(message):
    Event.update_event(EVENT_ID, name=message.text)

    event = Event.get_event(EVENT_ID)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_message(message.from_user.id, text=success_message)


def change_event_place(message):
    Event.update_event(EVENT_ID, place=message.text)

    event = Event.get_event(EVENT_ID)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_message(message.from_user.id, text=success_message)


def change_event_time(message):
    Event.update_event(EVENT_ID, time=message.text)

    event = Event.get_event(EVENT_ID)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_message(message.from_user.id, text=success_message)


def change_event_poster(message):
    file_id = message.photo[-1].file_id
    Event.update_event(EVENT_ID, poster=file_id)

    event = Event.get_event(EVENT_ID)

    success_message = f'''
        Изменение инфо про мероприятие {event.name}
        в {event.place}
        на {event.time}
        на удивление прошло успешно
    '''
    bot.send_photo(message.from_user.id, photo=file_id, caption=success_message)



