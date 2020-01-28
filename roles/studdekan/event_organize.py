from flask import Blueprint
from credentials import *
from db.event import Event
from keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers import restricted_studdekan


event_organize = Blueprint('event_organize', __name__)


@event_organize.route('/event_organize')
def event_organize_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text='Создать мероприятие', callback_data='new_event'))
    keyboard.add(InlineKeyboardButton(text='Удалить мероприятие', callback_data='delete_event'))
    keyboard.add(InlineKeyboardButton(text='Изменить мероприятие', callback_data='change_event'))
    keyboard.add(InlineKeyboardButton(text='Обьявить мероприятие', callback_data='alarm_event'))

    bot.send_message(message.from_user.id, text='Выбери', reply_markup=keyboard)


# creating
@bot.message_handler(commands=['org'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('new_event'))
@restricted_studdekan
def create_event(message):
    message = bot.edit_message_text(chat_id=message.from_user.id,
                          message_id=message.message.message_id,
                          text='Название мероприятия')

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
@restricted_studdekan
def delete_event(call):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'eventdelete_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Какое мероприятие удалить?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('eventdelete_') == True)
def delete_event_callback(call):
    event_id = call.data.split('_')[1]

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Мероприятие {Event.get_event(event_id).name} удалено')

    Event.delete_event(event_id)


# changing
@bot.message_handler(commands=['ech'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('change_event'))
@restricted_studdekan
def change_event(call):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'eventchange_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Какое мероприятие изменить?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('eventchange_') == True)
def event_callback(call):
    event_id = call.data.split('_')[1]
    event_name = Event.get_event(event_id).name

    change_event_keyboard = InlineKeyboardMarkup()
    change_event_keyboard.add(InlineKeyboardButton(text='Название', callback_data='name_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Место проведения', callback_data='place_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Дата проведения', callback_data='date_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Время проведения', callback_data='time_' + event_id))
    change_event_keyboard.add(InlineKeyboardButton(text='Постер', callback_data='poster_' + event_id))

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Что нужно изменить в мероприятии {event_name} ?',
                          reply_markup=change_event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('name_') or call.data.startswith('place_') or
                    call.data.startswith('date_') or call.data.startswith('time_') or call.data.startswith('poster_'))
def change_event_callback(call):
    event_id = call.data.split('_')[1]

    if call.data.startswith('name_'):
        message = bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Новое имя')
        bot.register_next_step_handler(message, change_event_name, event_id)
    elif call.data.startswith('place_'):
        message = bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Новое место')
        bot.register_next_step_handler(message, change_event_place, event_id)
    elif call.data.startswith('date_'):
        message = bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Новая дата')
        bot.register_next_step_handler(message, change_event_date, event_id)
    elif call.data.startswith('time_'):
        message = bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Новое время')
        bot.register_next_step_handler(message, change_event_time, event_id)
    elif call.data.startswith('poster_'):
        message = bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Новый постер')
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
@restricted_studdekan
def show_notification(call):
    event_keyboard = make_keyboard('event', Event.get_all_events(), 'alarm_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Какое мероприятие высветить?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('alarm_') == True)
def show_notification_callback(call):
    event_id = call.data.split('_')[1]
    event = Event.get_event(event_id)

    message = f'''
        {event.place} {event.time} будет {event.name}
    '''
    channel_id = '-1001104545927'
    bot.send_photo(channel_id, photo=event.poster, caption=message)
    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='ГОТОВО :D')
