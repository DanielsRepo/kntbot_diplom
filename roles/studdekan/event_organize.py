from flask import Blueprint
from credentials import *
from db.event import Event
from keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.role_helpers import restricted_studdekan
from emoji import emojize


event_organize = Blueprint('event_organize', __name__)


@event_organize.route('/event_organize')
def event_organize_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Створити захід {emojize(":white_check_mark:", use_aliases=True)}',
                                      callback_data='new_event'))
    keyboard.add(InlineKeyboardButton(text=f'Видалити захід {emojize(":x:", use_aliases=True)}',
                                      callback_data='delete_event'))
    keyboard.add(InlineKeyboardButton(text=f'Змінити захід {emojize(":pencil2:", use_aliases=True)}',
                                      callback_data='change_event'))
    keyboard.add(InlineKeyboardButton(text=f'Об’явити захід {emojize(":loudspeaker:", use_aliases=True)}',
                                      callback_data='alarm_event'))

    bot.send_message(chat_id=message.from_user.id, text='Вибери дію:', reply_markup=keyboard)


# creating
@bot.callback_query_handler(func=lambda call: call.data.startswith('new_event'))
@restricted_studdekan
def create_event(message):
    message = bot.edit_message_text(chat_id=message.from_user.id,
                                    message_id=message.message.message_id,
                                    text='Назва заходу')

    bot.register_next_step_handler(message, name_event)


def name_event(message):
    event = Event.add_event(name=message.text)
    message = bot.send_message(chat_id=message.from_user.id, text="Місце проведення")

    bot.register_next_step_handler(message, place_event, event.id)


def place_event(message, event_id):
    Event.update_event(event_id=event_id, place=message.text)

    message = bot.send_message(chat_id=message.from_user.id, text="Дата проведення")
    bot.register_next_step_handler(message, date_event, event_id)


def date_event(message, event_id):
    Event.update_event(event_id=event_id, date=message.text)

    message = bot.send_message(chat_id=message.from_user.id, text="Час проведення")
    bot.register_next_step_handler(message, time_event, event_id)


def time_event(message, event_id):
    Event.update_event(event_id=event_id, time=message.text)

    message = bot.send_message(chat_id=message.from_user.id, text="Баннер заходу")
    bot.register_next_step_handler(message, picture_event, event_id)


def picture_event(message, event_id):
    file_id = message.photo[-1].file_id

    Event.update_event(event_id=event_id, poster=file_id)

    bot.send_photo(chat_id=message.from_user.id, photo=file_id,
                   caption=f'Захід "{Event.get_event(event_id=event_id).name}" створено '
                           f'{emojize(":white_check_mark:", use_aliases=True)}')


# deleting
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_event'))
@restricted_studdekan
def delete_event(call):
    event_keyboard = make_keyboard(keyboard_type='event',
                                   elem_list=Event.get_all_events(),
                                   marker='eventdelete_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Який захід видалити?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('eventdelete_'))
def delete_event_callback(call):
    event_id = call.data.split('_')[1]

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Захід {Event.get_event(event_id).name} видалено '
                               f'{emojize(":white_check_mark:", use_aliases=True)}')

    Event.delete_event(event_id)


# changing
@bot.callback_query_handler(func=lambda call: call.data.startswith('change_event'))
@restricted_studdekan
def change_event(call):
    event_keyboard = make_keyboard(keyboard_type='event',
                                   elem_list=Event.get_all_events(),
                                   marker='eventchange_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Який захід змінити?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('eventchange_'))
def event_callback(call):
    event_id = call.data.split('_')[1]

    change_event_keyboard = InlineKeyboardMarkup()
    change_event_keyboard.add(InlineKeyboardButton(text='Назва заходу', callback_data=f'name_{event_id}'))
    change_event_keyboard.add(InlineKeyboardButton(text='Місце проведення', callback_data=f'place_{event_id}'))
    change_event_keyboard.add(InlineKeyboardButton(text='Дата проведення', callback_data=f'date_{event_id}'))
    change_event_keyboard.add(InlineKeyboardButton(text='Час проведення', callback_data=f'time_{event_id}'))
    change_event_keyboard.add(InlineKeyboardButton(text='Баннер заходу', callback_data=f'poster_{event_id}'))

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Що потрібно змінити в заході {Event.get_event(event_id=event_id).name}?',
                          reply_markup=change_event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith(('name_', 'place_', 'date_', 'time_', 'poster_')))
def change_event_callback(call):
    event_id = call.data.split('_')[1]

    if call.data.startswith('name_'):
        message = bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text='Нова назва')
        bot.register_next_step_handler(message, change_event_name, event_id)
    elif call.data.startswith('place_'):
        message = bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text='Нове місце')
        bot.register_next_step_handler(message, change_event_place, event_id)
    elif call.data.startswith('date_'):
        message = bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text='Нова дата')
        bot.register_next_step_handler(message, change_event_date, event_id)
    elif call.data.startswith('time_'):
        message = bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text='Новий час')
        bot.register_next_step_handler(message, change_event_time, event_id)
    elif call.data.startswith('poster_'):
        message = bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text='Новий баннер')
        bot.register_next_step_handler(message, change_event_poster, event_id)


def change_event_name(message, event_id):
    Event.update_event(event_id=event_id, name=message.text)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'Назву заходу змінено на "{Event.get_event(event_id=event_id).name}" '
                          f'{emojize(":white_check_mark:", use_aliases=True)}')


def change_event_place(message, event_id):
    Event.update_event(event_id=event_id, place=message.text)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'Місце проведення заходу змінено на {Event.get_event(event_id=event_id).place} '
                          f'{emojize(":white_check_mark:", use_aliases=True)}')


def change_event_date(message, event_id):
    Event.update_event(event_id=event_id, date=message.text)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'Дату проведення заходу змінено на {Event.get_event(event_id=event_id).date} '
                          f'{emojize(":white_check_mark:", use_aliases=True)}')


def change_event_time(message, event_id):
    Event.update_event(event_id=event_id, time=message.text)

    bot.send_message(chat_id=message.from_user.id,
                     text=f'Час проведення заходу змінено на {Event.get_event(event_id=event_id).time} '
                          f'{emojize(":white_check_mark:", use_aliases=True)}')


def change_event_poster(message, event_id):
    file_id = message.photo[-1].file_id
    Event.update_event(event_id=event_id, poster=file_id)

    bot.send_photo(message.from_user.id, photo=file_id, caption=f'Баннер заходу змінено '
                                                                f'{emojize(":white_check_mark:", use_aliases=True)}')


# notification
@bot.callback_query_handler(func=lambda call: call.data.startswith('alarm_event'))
@restricted_studdekan
def show_notification(call):
    event_keyboard = make_keyboard(keyboard_type='event',
                                   elem_list=Event.get_all_events(),
                                   marker='alarm_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Який захід оголосити?',
                          reply_markup=event_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('alarm_'))
def show_notification_callback(call):
    event_id = call.data.split('_')[1]
    event = Event.get_event(event_id)

    message = f'{event.name}\n' \
              f'Місце проведення: {event.place}\n' \
              f'Час проведення: {event.time}'

    bot.send_photo(chat_id='-1001104545927', photo=event.poster, caption=message)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Захід оголошено {emojize(":white_check_mark:", use_aliases=True)}')
