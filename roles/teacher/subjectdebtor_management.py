from flask import Blueprint
from credentials import bot
from database.group import Group
from database.student import Student
from database.subject import Subject
from database.subject_debtor import SubjectDebtor
from keyboards.keyboard import make_keyboard
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from helpers.xlsx_helper import get_fio

subject_debtors = Blueprint('subject_debtors', __name__)


@subject_debtors.route('/subject_debtors')
# ADD DEBTOR
def subject_debtor_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Додати боржника {emojize(":heavy_plus_sign:", use_aliases=True)}',
                                      callback_data='add_subject_debtor'))
    keyboard.add(InlineKeyboardButton(text=f'Видалити боржника {emojize(":heavy_minus_sign:", use_aliases=True)}',
                                      callback_data='delete_subject_debtor'))
    keyboard.add(InlineKeyboardButton(text=f'Боржники за предметом {emojize(":busts_in_silhouette:", use_aliases=True)}',
                                      callback_data='get_subject_debtors'))

    bot.send_message(message.from_user.id, text='Виберіть дію:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_subject_debtor'))
def add_subjectdebtor(call):
    subjects_keyboard = make_keyboard('subject', Subject.get_subjects(), 'debtorsubject_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть предмет:',
                          reply_markup=subjects_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtorsubject_'))
def get_subject_for_subjectdebt(call):
    subject_id = call.data.split('_')[1]

    group_keyboard = make_keyboard('student', Group.get_groups()[:4], f'subjectdebtorgroup_{subject_id}_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть групу:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('subjectdebtorgroup_'))
def get_group_for_subjectdebt(call):
    subject_id = call.data.split('_')[1]
    group_id = call.data.split('_')[2]

    student_keyboard = make_keyboard(keyboard_type='student',
                                     elem_list=[student for student in Student.get_students_by_group(group_id)],
                                     marker=f'debtorstudent_{subject_id}_{group_id}_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть студента:',
                          reply_markup=student_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('debtorstudent_'))
def add_debtor_callback(call):
    subject_id = call.data.split('_')[1]
    group_id = call.data.split('_')[2]
    debtor_id = call.data.split('_')[3]

    if not SubjectDebtor.add_debtor(debtor_id, subject_id):
        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text='Студент вже занесений до боржників')
    else:
        username = Student.get_student_by_id(debtor_id).username
        name = Student.get_student_by_id(debtor_id).name

        bot.edit_message_text(chat_id=call.from_user.id,
                              message_id=call.message.message_id,
                              text=f'Студент <b><a href="t.me/{username}">{name}</a></b> '
                                   f'групи <b>{Group.get_group_by_id(group_id)}</b> занесений до боржників по предмету '
                                   f'<b>{Subject.get_subject_by_id(subject_id)}</b> '
                                   f'{emojize(":white_check_mark:", use_aliases=True)}',
                              parse_mode='html')

# delete debtor
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_subject_debtor'))
def delete_debtor(call):
    subjects_keyboard = make_keyboard('subject', Subject.get_subjects(), 'deldebtorsubject_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть предмет:',
                          reply_markup=subjects_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('deldebtorsubject_'))
def choose_subject_callback(call):
    subject_id = call.data.split('_')[1]

    group_keyboard = InlineKeyboardMarkup(row_width=1)
    keys_list = []

    for group in Group.get_groups()[:4]:
        keys_list.append(InlineKeyboardButton(text=str(group.name), callback_data=f'subjectdeldebtorgroup_{subject_id}_' + str(group.id)))

    group_keyboard.add(*keys_list)

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть групу:',
                          reply_markup=group_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('subjectdeldebtorgroup_'))
def choose_debtor_group_callback(call):
    subject_id = call.data.split('_')[1]
    group_id = call.data.split('_')[2]

    debtor_list = SubjectDebtor.get_debtors_by_subject_group(subject_id, group_id)
    debtor_list_keyboard = InlineKeyboardMarkup()

    if not debtor_list:
        message_text = 'В цій групі немає боржників'
    else:
        debtor_list_keyboard = make_keyboard(keyboard_type='student',
                                             elem_list=debtor_list,
                                             marker=f'delsubjectdebtor_{subject_id}_{group_id}_')
        message_text = 'Виберіть боржника:'

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=message_text,
                          reply_markup=debtor_list_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delsubjectdebtor_'))
def choose_debtor_delete_callback(call):
    subject_id = call.data.split('_')[1]
    group_id = call.data.split('_')[2]
    student_id = call.data.split('_')[3]

    SubjectDebtor.delete_debtor(subject_id, student_id)

    username = Student.get_student_by_id(student_id).username
    name = Student.get_student_by_id(student_id).name

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=f'Студент <b><a href="t.me/{username}">{name}</a></b> '
                               f'групи <b>КНТ-{Group.get_group_by_id(group_id)}</b> '
                               f'видалений з боржників по предмету <b>{Subject.get_subject_by_id(subject_id)}</b> '
                               f'{emojize(":white_check_mark:", use_aliases=True)}',
                          parse_mode='html')


# get debtors
@bot.callback_query_handler(func=lambda call: call.data.startswith('get_subject_debtors'))
def get_debtors_by_subject(call):
    subjects_keyboard = make_keyboard('subject', Subject.get_subjects(), 'getdebtorsubject_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Виберіть предмет:',
                          reply_markup=subjects_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('getdebtorsubject_'))
def show_debtors_by_subject(call):
    subject_id = call.data.split('_')[1]
    subject = Subject.get_subject_by_id(subject_id)

    debtors_list = SubjectDebtor.get_debtors_by_subject(subject_id=subject_id)

    if not debtors_list:
        message_text = f'По предмету <b>{subject}</b> немає боржників'
    else:
        debts_dict = {}
        for debt in debtors_list:
            debtor = Student.get_student_by_id(debt.student_id)
            group = Group.get_group_by_id(debtor.group_id)

            debts_dict.setdefault(group, []).append(get_fio(debtor.name))

        message_text = f'Боржники за предметом <b>{subject}</b>:\n\n'
        for group in debts_dict:
            message_text += ''.join(f'<b>КНТ-{group}:</b> {", ".join(debts_dict[group])}\n')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=message_text,
                          parse_mode='html')
