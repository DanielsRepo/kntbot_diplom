from flask import Blueprint
from credentials import bot
from db.group import Group
from db.student import Student
from db.headman import Headman
from keyboard import make_keyboard, make_role_replykeyboard, studdekan_buttons
from helpers.role_helpers import restricted_studdekan
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from emoji import emojize

headmans = Blueprint('headmans', __name__)


@headmans.route('/headmans')
def headman_keyboard(message):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(InlineKeyboardButton(text=f'Призначити старосту {emojize(":white_check_mark:", use_aliases=True)}',
                                      callback_data='assign_headman'))
    keyboard.add(InlineKeyboardButton(text=f'Змінити старосту {emojize(":repeat:", use_aliases=True)}',
                                      callback_data='change_headman'))
    keyboard.add(InlineKeyboardButton(text=f'Переглянути старосту {emojize(":bust_in_silhouette:", use_aliases=True)}',
                                      callback_data='get_headman'))

    bot.send_message(chat_id=message.from_user.id, text='Вибери дію:', reply_markup=keyboard)


# add headman
@bot.callback_query_handler(func=lambda call: call.data.startswith('assign_headman'))
@restricted_studdekan
def add_headman(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='headmangroup_')

    bot.send_message(chat_id=call.from_user.id,
                     text='Вибери групу:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, headman_group_callback)


def headman_group_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        if not Headman.get_headman_by_group(group_id):
            student_keyboard = make_keyboard(keyboard_type='student',
                                             elem_list=Student.get_students_by_group(group_id),
                                             marker=f'headman_{Group.get_group_by_id(group_id)}_')

            bot.send_message(chat_id=message.from_user.id,
                             text='Вибери старосту:',
                             reply_markup=student_keyboard)
        else:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=f'Змінити старосту {emojize(":repeat:", use_aliases=True)}',
                                              callback_data='change_headman'))

            bot.send_message(chat_id=message.from_user.id,
                             text='Цій групі вже призначено старосту.\n'
                                  'Якщо потрібно його змінити, скористайся командою '
                                  f'{emojize(":point_down:", use_aliases=True)}',
                             reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('headman_'))
def add_headman_callback(call):
    group = call.data.split('_')[1]
    headman_id = call.data.split('_')[2]

    Headman.add_headman(headman_id)

    username = Student.get_student_by_id(headman_id).username
    name = Student.get_student_by_id(headman_id).name

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'<a href="t.me/{username}">{name}</a> призначений старостою групи {group} '
                               f'{emojize(":white_check_mark:", use_aliases=True)}',
                          parse_mode='html')
    bot.send_message(chat_id=call.from_user.id,
                     text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(studdekan_buttons))


# change headman
@bot.callback_query_handler(func=lambda call: call.data.startswith('change_headman'))
@restricted_studdekan
def change_headman(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='chheadgroup_')

    bot.send_message(chat_id=call.from_user.id,
                     text='Змінити старосту групи:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, change_headman_group_callback)


def change_headman_group_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        student_keyboard = make_keyboard(keyboard_type='student',
                                         elem_list=Student.get_students_by_group(group_id),
                                         marker=f'chheadman_{Group.get_group_by_id(group_id)}_')

        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери нового старосту:',
                         reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('chheadman_'))
def change_headman_callback(call):
    group = call.data.split('_')[1]
    new_headman_id = call.data.split('_')[2]

    Headman.change_headman(new_headman_id)

    username = Student.get_student_by_id(new_headman_id).username
    name = Student.get_student_by_id(new_headman_id).name

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'<a href="t.me/{username}">{name}</a> '
                               f'призначений старостою групи {group} '
                               f'{emojize(":white_check_mark:", use_aliases=True)}',
                          parse_mode='html')
    bot.send_message(chat_id=call.from_user.id,
                     text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(studdekan_buttons))


# get headman
@bot.callback_query_handler(func=lambda call: call.data.startswith('get_headman'))
@restricted_studdekan
def get_headman(call):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='getheadgroup_')

    bot.send_message(chat_id=call.from_user.id, text='Вибери группу:', reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, get_headman_group_callback)


def get_headman_group_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        headman = Headman.get_headman_by_group(group_id)

        if not headman:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=f'Призначити старосту '
                                                   f'{emojize(":white_check_mark:", use_aliases=True)}',
                                              callback_data='assign_headman'))

            bot.send_message(chat_id=message.from_user.id,
                             text=f'Групі {group} непризначено старосту.\n'
                                  'Для призначення старости скористайся командою '
                                  f'{emojize(":point_down:", use_aliases=True)}',
                             reply_markup=keyboard)
        else:
            username = Student.get_student_by_id(headman.student_id).username
            name = Student.get_student_by_id(headman.student_id).name

            bot.send_message(chat_id=message.from_user.id,
                             text=f'Староста групи {group}: <a href="t.me/{username}">{name}</a>',
                             parse_mode='html')
            bot.send_message(chat_id=message.from_user.id,
                             text='Вибери пункт меню:',
                             reply_markup=make_role_replykeyboard(studdekan_buttons))
