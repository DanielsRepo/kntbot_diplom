from flask import Blueprint
from credentials import bot
from db.headman import Headman
from db.group import Group
from db.student import Student
from keyboard import make_keyboard, make_headman_rate_keyboard, make_role_replykeyboard, dekanat_buttons
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

headman_management = Blueprint('headman_management', __name__)


@headman_management.route('/headman_management')
@bot.callback_query_handler(func=lambda call: call.data.startswith('assign_headman'))
def rate_headman(message):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='rateheadman_')

    bot.send_message(chat_id=message.from_user.id, text='Староста групи:', reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(message.from_user.id, rate_headman_callback)


def rate_headman_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Виберіть пункт меню:',
                         reply_markup=make_role_replykeyboard(dekanat_buttons))
    else:
        headman = Headman.get_headman_by_group(group_id)
        if headman is None:
            bot.send_message(chat_id=message.from_user.id,
                             text='Старосту не призначено\nВиберіть пункт меню:',
                             reply_markup=make_role_replykeyboard(dekanat_buttons))
        else:
            headman_name = Student.get_student_by_id(headman.student_id).name

            headman_rate_keyboard = make_headman_rate_keyboard(group_id=group_id, rating=headman.rating)

            bot.send_message(chat_id=message.from_user.id,
                             text=f'Староста групи КНТ-{group} {headman_name}',
                             reply_markup=headman_rate_keyboard)

            bot.send_message(chat_id=message.from_user.id,
                             text='Виберіть пункт меню:',
                             reply_markup=make_role_replykeyboard(dekanat_buttons))


@bot.callback_query_handler(func=lambda call: call.data.startswith(('rateminus_', 'rateplus_')))
def rate_headman_sign_callback(call):
    group_id = call.data.split('_')[1]
    group = Group.get_group_by_id(group_id)

    headman = Headman.get_headman_by_group(group_id)
    if headman is None:
        bot.send_message(chat_id=call.from_user.id,
                         text='Старосту не призначено\nВиберіть пункт меню:',
                         reply_markup=make_role_replykeyboard(dekanat_buttons))
        return

    headman_name = Student.get_student_by_id(headman.student_id).name

    if call.data.startswith('rateminus_'):
        Headman.rate_headman(group_id, '-')
    elif call.data.startswith('rateplus_'):
        if headman.rating != 6:
            Headman.rate_headman(group_id, '+')
        else:
            bot.edit_message_text(chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  text=f'Цей староста вже має максимальний рейтинг')
            return

    headman_rate_keyboard = make_headman_rate_keyboard(group_id=group_id, rating=headman.rating)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Староста групи КНТ-{group} {headman_name}',
                          reply_markup=headman_rate_keyboard)

    bot.send_message(chat_id=374464076, text='#dekanatchangedrate')


@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_journal'))
def remind_journal(message):
    remind_keyboard = InlineKeyboardMarkup()

    remind_keyboard.add(InlineKeyboardButton(text='Вибрати старосту', callback_data='remind_one'))
    remind_keyboard.add(InlineKeyboardButton(text='Всім', callback_data='remind_all'))

    bot.send_message(chat_id=message.from_user.id, text='Кому нагадати?', reply_markup=remind_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_one'))
def remind_one(call):
    group_keyboard = make_keyboard('group', Group.get_groups(), 'remindonegroup_')

    bot.send_message(chat_id=call.from_user.id,
                     text='Виберіть старосту якої групи:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, remind_one_callback)


def remind_one_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Виберіть пункт меню:',
                         reply_markup=make_role_replykeyboard(dekanat_buttons))
    else:
        headman = Headman.get_headman_by_group(group_id)
        if headman is None:
            bot.clear_step_handler_by_chat_id(message.from_user.id)
            bot.send_message(chat_id=message.from_user.id,
                             text='Старосту не призначено\nВиберіть пункт меню:',
                             reply_markup=make_role_replykeyboard(dekanat_buttons))
            return

        headman_name = Student.get_student_by_id(headman.student_id).name

        bot.send_message(chat_id=message.from_user.id,
                         text=f'Старості групи КНТ-{group} '
                              f'{headman_name} було відправлено нагадування'
                              f'{emojize(":white_check_mark:", use_aliases=True)}')

        bot.send_message(chat_id=message.from_user.id,
                         text='Виберіть пункт меню:',
                         reply_markup=make_role_replykeyboard(dekanat_buttons))

        bot.send_message(chat_id=headman.student_id,
                         text='Повідомлення від деканату '
                              f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}\n\n'
                              'Заповни журнал')

        bot.send_message(chat_id=374464076, text='#dekanatremindone')


@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_all'))
def remind_all(call):
    for headman_id in Headman.get_all_headmans():
        try:
            bot.send_message(chat_id=headman_id,
                             text='Повідомлення від деканату '
                                  f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}\n\n'
                                  'Заповни журнал')
        except ApiException:
            continue

    bot.send_message(chat_id=call.from_user.id,
                     text='Всім старостам було відправлено нагадування '
                          f'{emojize(":white_check_mark:", use_aliases=True)}')

    bot.send_message(chat_id=call.from_user.id,
                     text='Виберіть пункт меню:',
                     reply_markup=make_role_replykeyboard(dekanat_buttons))

    bot.send_message(chat_id=374464076, text='#dekanatremindall')


def send_file(message):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='sendfile_')

    bot.send_message(chat_id=message.from_user.id, text='Виберіть старосту групи:', reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(message.from_user.id, send_file_callback)


def send_file_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Виберіть пункт меню:',
                         reply_markup=make_role_replykeyboard(dekanat_buttons))
    else:
        headman = Headman.get_headman_by_group(group_id)
        if headman is None:
            bot.clear_step_handler_by_chat_id(message.from_user.id)
            bot.send_message(chat_id=message.from_user.id,
                             text='Старосту не призначено\nВиберіть пункт меню:',
                             reply_markup=make_role_replykeyboard(dekanat_buttons))
            return

        message = bot.send_message(chat_id=message.from_user.id,
                                   text='Відправте файл боту і він його передасть старості '
                                        f'{emojize(":incoming_envelope:", use_aliases=True)}',
                                   reply_markup=make_role_replykeyboard(dekanat_buttons))

        bot.register_next_step_handler(message, send_file_headman, headman.student_id)


def send_file_headman(message, headman_id):
    if message.text == '/cancel':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Дія була скасована {emojize(":white_check_mark:", use_aliases=True)}')
        bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
    elif message.content_type not in ['photo', 'document']:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Файл не відправлено {emojize(":x:", use_aliases=True)}\n\n'
                              'Файл має бути фото чи документом\n'
                              'Відправте файл боту і він його передасть старості\n\n'
                              'Щоб скасувати дію можна скористатися командою /cancel')

        bot.register_next_step_handler(message, send_file_headman, headman_id)
    else:
        caption = '' if message.caption is None else message.caption

        if message.content_type == 'document':
            bot.send_document(chat_id=headman_id,
                              data=message.document.file_id,
                              caption=f'Повідомлення від деканату '
                                      f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}'
                                      f'\n\n{caption}')
        elif message.content_type == 'photo':
            bot.send_photo(chat_id=headman_id,
                           photo=message.photo[-1].file_id,
                           caption=f'Повідомлення від деканату '
                                   f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}'
                                   f'\n\n{caption}')

        bot.send_message(chat_id=message.from_user.id,
                         text=f'Файл відправлений старості {emojize(":white_check_mark:", use_aliases=True)}')

        bot.send_message(chat_id=374464076, text='#dekanatsentfile')
