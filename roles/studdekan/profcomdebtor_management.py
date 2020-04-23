from flask import Blueprint
from credentials import bot
from database.group import Group
from database.student import Student
from database.profcom_debtor import ProfcomDebtor
from keyboards.keyboard import make_keyboard, make_role_replykeyboard, studdekan_buttons
from helpers.role_helper import restricted_studdekan
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

debtors = Blueprint('debtors', __name__)


@debtors.route('/debtors')
def profcom_debtor_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Додати боржника {emojize(":heavy_plus_sign:", use_aliases=True)}',
                                      callback_data='add_debtor'))
    keyboard.add(InlineKeyboardButton(text=f'Видалити боржника {emojize(":heavy_minus_sign:", use_aliases=True)}',
                                      callback_data='delete_debtor'))
    keyboard.add(InlineKeyboardButton(text=f'Боржники за групою {emojize(":busts_in_silhouette:", use_aliases=True)}',
                                      callback_data='debtors_of_group'))

    bot.send_message(message.from_user.id, text='Вибери дію:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_debtor'))
@restricted_studdekan
# add debtor
def add_profcomdebtor(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='debtorgroup_')

    bot.send_message(chat_id=call.from_user.id,
                     text='Вибери групу:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, get_profcomdebtor_for_add)


def get_group_for_profcomdebt(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        student_keyboard = make_keyboard(keyboard_type='student',
                                         elem_list=[student for student in Student.get_students_by_group(group_id)],
                                         marker=f'debtor_{Group.get_group_by_id(group_id)}_')

        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери студента:', reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtor_'))
def get_profcomdebtor_for_add(call):
    group = call.data.split('_')[1]
    debtor_id = call.data.split('_')[2]

    if ProfcomDebtor.debtor_exists(debtor_id):
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text='Студент вже занесений до боржників')

        bot.send_message(chat_id=call.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text='Введи борг студента')

        bot.register_next_step_handler_by_chat_id(call.from_user.id, save_profcomdebtor, debtor_id, group)


def save_profcomdebtor(message, debtor_id, group):
    debt = message.text

    ProfcomDebtor.add_debtor(debtor_id, debt)

    username = Student.get_student_by_id(debtor_id).username
    name = Student.get_student_by_id(debtor_id).name

    bot.send_message(chat_id=message.from_user.id,
                     text=f'Студент <a href="t.me/{username}">{name}</a> '
                          f'групи {group} занесений до боржників '
                          f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}',
                     parse_mode='html')

    bot.send_message(chat_id=message.from_user.id,
                     text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(studdekan_buttons))


# delete debtor
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_debtor'))
@restricted_studdekan
def delete_profcomdebtor(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='deldebtorgroup_')

    bot.send_message(chat_id=call.from_user.id,
                     text='Вибери групу:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, get_group_for_del_profcomdebt)


def get_group_for_del_profcomdebt(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        debtor_list = ProfcomDebtor.get_debtors_by_group(group_id)
        debtor_list_keyboard = InlineKeyboardMarkup()

        if not debtor_list:
            message_text = 'В цій групі немає боржників'
        else:
            debtor_list_keyboard = make_keyboard(keyboard_type='student',
                                                 elem_list=debtor_list,
                                                 marker='deldebtor_')
            message_text = 'Вибери боржника:'

        bot.send_message(chat_id=message.from_user.id,
                         text=message_text, reply_markup=debtor_list_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('deldebtor_'))
def get_profcomdebtor_for_del(call):
    debtor_id = call.data.split('_')[1]

    group = Group.get_group_by_id(Student.get_student_by_id(debtor_id).group_id)
    username = Student.get_student_by_id(debtor_id).username
    name = Student.get_student_by_id(debtor_id).name

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Студент <a href="t.me/{username}">{name}</a> '
                               f'групи {group} видалений з боржників '
                               f'{emojize(":heavy_exclamation_mark:", use_aliases=True)}',
                          parse_mode='html')

    ProfcomDebtor.delete_debtor(debtor_id)

    bot.send_message(chat_id=call.from_user.id,
                     text='Вибери пункт меню:',
                     reply_markup=make_role_replykeyboard(studdekan_buttons))


# get debtors
@bot.callback_query_handler(func=lambda call: call.data.startswith('debtors_of_group'))
@restricted_studdekan
def get_debtors_by_group(call):
    group_keyboard = make_keyboard(keyboard_type='group',
                                   elem_list=Group.get_groups(),
                                   marker='grdebtor_')

    bot.send_message(chat_id=call.from_user.id,
                     text='Вибери групу:',
                     reply_markup=group_keyboard)

    bot.register_next_step_handler_by_chat_id(call.from_user.id, show_debtors_by_group_callback)


def show_debtors_by_group_callback(message):
    group = message.text
    group_id = Group.get_id_by_group(group)

    if group_id is False:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
    else:
        debtors_list = ProfcomDebtor.get_debtors_by_group(group_id)

        if not debtors_list:
            message_text = 'В цій групі немає боржників'
        else:
            debtors_str = ''.join((f'<a href="t.me/{debtor.username}">'
                                   f'{debtor.name}</a> - {ProfcomDebtor.get_debt(debtor.id)}\n' for debtor in debtors_list))
            message_text = f'Боржники групи {group}:\n{debtors_str}'

        bot.send_message(chat_id=message.from_user.id,
                         text=message_text,
                         parse_mode='html',
                         disable_web_page_preview=True)

        bot.send_message(chat_id=message.from_user.id,
                         text='Вибери пункт меню:',
                         reply_markup=make_role_replykeyboard(studdekan_buttons))
