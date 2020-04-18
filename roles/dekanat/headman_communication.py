from flask import Blueprint
from credentials import bot
from database.headman import Headman
from database.group import Group
from database.student import Student
from keyboards.keyboard import make_keyboard, make_headman_rate_keyboard, make_role_replykeyboard, dekanat_buttons
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from helpers.role_helper import restricted_dekanat
headman_management = Blueprint('headman_management', __name__)


@headman_management.route('/headman_management')
@bot.callback_query_handler(func=lambda call: call.data.startswith('assign_headman'))
@restricted_dekanat
def rate_headman(message):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='rateheadman_')

    bot.send_message(chat_id=message.from_user.id, text='Староста групи:', reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(message.from_user.id, get_headman_for_rate)


def get_headman_for_rate(message):
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
def assign_headman_rating(call):
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


def remind_journal(message):
    remind_journal_keyboard = InlineKeyboardMarkup()

    remind_journal_keyboard.add(InlineKeyboardButton(text='Вибрати старосту', callback_data='remind_one'))
    remind_journal_keyboard.add(InlineKeyboardButton(text='Всім', callback_data='remind_all'))

    bot.send_message(chat_id=message.from_user.id,
                     text='Кому нагадати?',
                     reply_markup=remind_journal_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remind_one'))
def remind_one(call):
    group_keyboard = make_keyboard('group', Group.get_groups(), 'remindonegroup_')

    bot.send_message(chat_id=call.from_user.id,
                     text='Виберіть старосту якої групи:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, get_headman_for_remind)


def get_headman_for_remind(message):
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

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Всім старостам було відправлено нагадування '
                               f'{emojize(":white_check_mark:", use_aliases=True)}')

    bot.send_message(chat_id=call.from_user.id,
                     text='Виберіть пункт меню:',
                     reply_markup=make_role_replykeyboard(dekanat_buttons))

    bot.send_message(chat_id=374464076, text='#dekanatremindall')


def dekanat_send_message_or_file(message):
    send_file_keyboard = InlineKeyboardMarkup()

    send_file_keyboard.add(InlineKeyboardButton(text='Вибрати старосту', callback_data='send_to_one'))
    send_file_keyboard.add(InlineKeyboardButton(text='Тільки 4 курсу', callback_data='send_fourcourse'))
    send_file_keyboard.add(InlineKeyboardButton(text='Тільки магістрам', callback_data='send_magistr'))
    send_file_keyboard.add(InlineKeyboardButton(text='Всім', callback_data='send_all'))

    bot.send_message(chat_id=message.from_user.id, text='Кому відправити?', reply_markup=send_file_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('send_to_one'))
def send_message_or_file_to_one(call):
    group_keyboard = make_keyboard(keyboard_type='group', elem_list=Group.get_groups(), marker='sendmessagefile_')

    bot.send_message(chat_id=call.from_user.id, text='Староста групи:', reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, get_headman_for_message_or_file)


@bot.callback_query_handler(func=lambda call: call.data.startswith('sendmessagefile_'))
def get_headman_for_message_or_file(message):
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
                                   text='Відправте файл або повідомлення боту і він передасть старості '
                                        f'{emojize(":incoming_envelope:", use_aliases=True)}',
                                   reply_markup=make_role_replykeyboard(dekanat_buttons))

        bot.register_next_step_handler(message, send_message_or_file_func, [headman.student_id])


@bot.callback_query_handler(func=lambda call: call.data.startswith('send_fourcourse'))
def send_message_or_file_to_fourcourse(message):
    headmans = []
    for group in Group.get_groups():
        group_name = group.name
        if group_name[len(group_name) - 1] == '6' or '7сп' in group_name:
            try:
                headmans.append(Headman.get_headman_by_group(group.id).student_id)
            except AttributeError:
                continue

    message = bot.send_message(chat_id=message.from_user.id,
                               text='Відправте файл або повідомлення боту і він передасть старостам '
                                    f'{emojize(":incoming_envelope:", use_aliases=True)}')

    bot.register_next_step_handler(message, send_message_or_file_func, headmans)


@bot.callback_query_handler(func=lambda call: call.data.startswith('send_magistr'))
def send_message_or_file_to_magistrs(message):
    headmans = []
    for group in Group.get_groups():
        group_name = group.name
        if group_name[len(group_name) - 1] == 'м':
            try:
                headmans.append(Headman.get_headman_by_group(group.id).student_id)
            except AttributeError:
                continue

    message = bot.send_message(chat_id=message.from_user.id,
                               text='Відправте файл або повідомлення боту і він передасть старостам '
                                    f'{emojize(":incoming_envelope:", use_aliases=True)}')

    bot.register_next_step_handler(message, send_message_or_file_func, headmans)


@bot.callback_query_handler(func=lambda call: call.data.startswith('send_all'))
def send_message_or_file_to_all(message):
    headmans = []
    for group in Group.get_groups():
        try:
            headmans.append(Headman.get_headman_by_group(group.id).student_id)
        except AttributeError:
            continue

    message = bot.send_message(chat_id=message.from_user.id,
                               text='Відправте файл або повідомлення боту і він передасть старостам '
                                    f'{emojize(":incoming_envelope:", use_aliases=True)}')

    bot.register_next_step_handler(message, send_message_or_file_func, headmans)


def send_message_or_file_func(message, headman_list):
    if message.text == '/cancel':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Дія була скасована {emojize(":white_check_mark:", use_aliases=True)}')
        bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
    else:
        for headman_id in headman_list:
            if message.content_type not in ['text', 'photo', 'document']:
                bot.send_message(chat_id=message.from_user.id,
                                 text=f'Файл/повідомлення не відправлено {emojize(":x:", use_aliases=True)}\n\n'
                                      'Некорректний формат\n'
                                      'Відправте файл/повідомлення боту і він передасть старості\n\n'
                                      'Щоб скасувати дію можна скористатися командою /cancel')

                bot.register_next_step_handler(message, send_message_or_file_func, headman_list)
            else:
                caption = '' if message.caption is None else message.caption

                if message.content_type == 'text':
                    bot.send_message(chat_id=headman_id,
                                     text=f'Повідомлення від деканату '
                                          f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}'
                                          f'\n\n{message.text}')
                    bot.send_message(chat_id=message.from_user.id,
                                     text=f'Повідомлення було відправлено '
                                          f'{emojize(":white_check_mark:", use_aliases=True)}')
                elif message.content_type == 'document':
                    bot.send_document(chat_id=headman_id,
                                      data=message.document.file_id,
                                      caption=f'Повідомлення від деканату '
                                              f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}'
                                              f'\n\n{caption}')
                    bot.send_message(chat_id=message.from_user.id,
                                     text=f'Файл було відправлено {emojize(":white_check_mark:", use_aliases=True)}')
                elif message.content_type == 'photo':
                    bot.send_photo(chat_id=headman_id,
                                   photo=message.photo[-1].file_id,
                                   caption=f'Повідомлення від деканату '
                                           f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}'
                                           f'\n\n{caption}')
                    bot.send_message(chat_id=message.from_user.id,
                                     text=f'Фото було відправлено {emojize(":white_check_mark:", use_aliases=True)}')

        bot.send_message(chat_id=message.from_user.id,
                         text='Виберіть пункт меню:',
                         reply_markup=make_role_replykeyboard(dekanat_buttons))

        bot.send_message(chat_id=374464076, text='#dekanatsentfile')
