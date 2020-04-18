from flask import Blueprint
from credentials import bot
from database.event import Event
from database.event_visitor import EventVisitor
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from keyboards.keyboard import menu_buttons
from database.group import Group
from database.student import Student

events = Blueprint('events', __name__)


@events.route('/events')
# get_events_schelude
def get_events_schelude(message):
    event_list = Event.get_all_events()

    if event_list:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keys_list = []

        for event in event_list:
            keys_list.append(InlineKeyboardButton(text=event.name, callback_data=f'schelude_{event.id}'))
            keys_list.append(InlineKeyboardButton(text=event.date, callback_data=f'schelude_{event.id}'))

        keyboard.add(*keys_list)

        bot.send_message(chat_id=message.from_user.id,
                         text=f'{emojize(":man_juggling:", use_aliases=True)} Розклад заходів '
                              f'{emojize(":performing_arts:", use_aliases=True)}',
                         reply_markup=keyboard)
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text='На даний час ніяких заходів не заплановано')


@bot.callback_query_handler(func=lambda call: call.data.startswith('schelude_'))
def get_event_info(call):
    event_id = call.data.split('_')[1]
    event = Event.get_event(event_id)

    message = f'<b> {event.name} </b>\n' \
              f'Місце проведення: {event.place}\n' \
              f'Дата: {event.date}\n' \
              f'Час: {event.time}'

    if EventVisitor.check_visitor(event_id=event_id, student_id=call.from_user.id) is False:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=f'{emojize(":pencil2:", use_aliases=True)} Зареєструватися',
                                          callback_data=f'regon_{event.id}'))

        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text=message,
                              reply_markup=keyboard, parse_mode='html')
    else:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=f'{emojize(":x:", use_aliases=True)} Відмінити реєстрацію',
                                          callback_data=f'cancelregevent_{event.id}'))

        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text=message,
                              reply_markup=keyboard, parse_mode='html')


# registration
@bot.callback_query_handler(func=lambda call: call.data.startswith('regon_'))
def register_on_event(call):
    event_id = call.data.split('_')[1]
    chat_id = call.from_user.id

    if Group.get_group_by_id(Student.get_student_by_id(chat_id).group_id) == 'other':
        message = bot.send_message(chat_id=chat_id,
                                   text="Введіть прізвище ім'я факультет групу\n"
                                        "<b>Наприклад:</b> <i>Петров Петро ФЕУ 123</i>",
                                   parse_mode='html')
        bot.register_next_step_handler(message, reg_on_event_other, event_id)
    else:
        EventVisitor.add_visitor(event_id, chat_id)

        bot.edit_message_text(chat_id=chat_id,
                              message_id=call.message.message_id,
                              text=f'Реєстрація пройшла успішно {emojize(":white_check_mark:", use_aliases=True)}')

        user = Student.get_student_by_id(chat_id)
        bot.send_message(chat_id=374464076,
                         text=f'#regonevent <a href="t.me/{user.username}">{user.name}</a> '
                              f'КНТ-{Group.get_group_by_id(user.group_id)}',
                         parse_mode='html',
                         disable_web_page_preview=True)


def reg_on_event_other(message, event_id):
    if message.text.startswith('/') or message.text in menu_buttons:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Дія була скасована {emojize(":white_check_mark:", use_aliases=True)}')
        bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
    else:
        EventVisitor.add_visitor(event_id, message.from_user.id, message.text)

        bot.send_message(chat_id=message.from_user.id,
                         text=f'Реєстрація пройшла успішно {emojize(":white_check_mark:", use_aliases=True)}')

        bot.send_message(chat_id=374464076,
                         text=f'#regonevent otherfac',
                         parse_mode='html',
                         disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('cancelregevent_'))
def cancel_reg_on_event(call):
    event_id = call.data.split('_')[1]

    EventVisitor.delete_visitor(event_id, call.from_user.id)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Реєстрація скасована {emojize(":white_check_mark:", use_aliases=True)}')

    user = Student.get_student_by_id(call.from_user.id)
    bot.send_message(chat_id=374464076,
                     text=f'#cancelregevent <a href="t.me/{user.username}">{user.name}</a> '
                          f'КНТ-{Group.get_group_by_id(user.group_id)}',
                     parse_mode='html',
                     disable_web_page_preview=True)
