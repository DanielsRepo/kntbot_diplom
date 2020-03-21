from flask import Blueprint
from credentials import bot
from database.group import Group
from database.student import Student
from database.subject import Subject
from telebot.apihelper import ApiException
from keyboards.keyboard import make_keyboard
from emoji import emojize
import os
from pathlib import Path

student_communication = Blueprint('student_communication', __name__)


@student_communication.route('/student_communication')
# SEND METHODS FILE
def send_message_or_file(message):
    subjects_keyboard = make_keyboard('subject', Subject.get_subjects(), 'methodsubject_')

    bot.send_message(chat_id=message.from_user.id,
                     text='Виберіть предмет:',
                     reply_markup=subjects_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('methodsubject_'))
def choose_methodsubject_callback(call):
    subject_id = call.data.split('_')[1]

    message = bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text='Відправте файл або повідомлення боту і він його передасть '
                                         'всім студентам цього предмету '
                                         f'{emojize(":incoming_envelope:", use_aliases=True)}')

    bot.register_next_step_handler(message, send_message_or_file_func, subject_id)


def send_message_or_file_func(message, subject_id):
    if message.text == '/cancel':
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Дія була скасована {emojize(":white_check_mark:", use_aliases=True)}')
        bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
    elif message.content_type not in ['text', 'photo', 'document']:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Файл/повідомлення не відправлено {emojize(":x:", use_aliases=True)}\n\n'
                              'Некорректний формат\n'
                              'Відправте файл/повідомлення боту і він його передасть всім студентам цього предмету\n\n'
                              'Щоб скасувати дію можна скористатися командою /cancel')

        bot.register_next_step_handler(message, send_message_or_file_func, subject_id)
    else:
        subject = Subject.get_subject_by_id(subject_id)

        for group in Group.get_groups():
            for student in Student.get_students_by_group(group.id):
                try:
                    caption = '' if message.caption is None else message.caption

                    if message.content_type == 'text':
                        bot.send_message(chat_id=student.id,
                                         text=f'Повідомлення по предмету {subject}:\n\n{message.text}')
                        bot.send_message(chat_id=message.from_user.id,
                                         text=f'Повідомлення було відправлено '
                                              f'{emojize(":white_check_mark:", use_aliases=True)}')
                    elif message.content_type == 'document':
                        bot.send_document(chat_id=student.id,
                                          data=message.document.file_id,
                                          caption=f'Методичний матеріал з предмету {subject} '
                                                  f'\n\n{caption}')
                        bot.send_message(chat_id=message.from_user.id,
                                         text=f'Файл було відправлено {emojize(":white_check_mark:", use_aliases=True)}')

                        save_file_to_local(message.document.file_id, subject)
                    elif message.content_type == 'photo':
                        bot.send_photo(chat_id=student.id,
                                       photo=message.photo[-1].file_id,
                                       caption=f'Методичний матеріал з предмету {subject} '
                                               f'\n\n{caption}')
                        bot.send_message(chat_id=message.from_user.id,
                                         text=f'Фото було відправлено {emojize(":white_check_mark:", use_aliases=True)}')

                        save_file_to_local(message.photo[-1].file_id, subject)
                except ApiException:
                    continue


def save_file_to_local(file_id, subject):
    bot_file_path = bot.get_file(file_id).file_path
    downloaded_file = bot.download_file(bot_file_path)
    file_extension = bot_file_path.split('.')[1]

    local_file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tmp'
    subject_path = f'{local_file_path}/{subject}'
    Path(subject_path).mkdir(parents=True, exist_ok=True)

    file_count = len(next(os.walk(subject_path))[2])
    number = '' if file_count == 0 else f'_{file_count + 1}'

    with open(f'{subject_path}/{subject}{number}.{file_extension}', 'wb') as new_file:
        new_file.write(downloaded_file)

