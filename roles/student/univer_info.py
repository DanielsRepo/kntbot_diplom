from flask import Blueprint
from credentials import bot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize


univer_info = Blueprint('univer_info', __name__)


@univer_info.route('/univer_info')
def univer_info_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Відділ бухгалтерського обліку {emojize(":dollar:", use_aliases=True)}',
                                      callback_data='accounting'))
    keyboard.add(InlineKeyboardButton(text=f'Центр сприяння працевлаштуванню {emojize(":fax:", use_aliases=True)}',
                                      callback_data='employment'))
    keyboard.add(InlineKeyboardButton(text=f'Профком студентів {emojize(":shield:", use_aliases=True)}',
                                      callback_data='profcom'))
    keyboard.add(InlineKeyboardButton(text=f'Сайт НУ «ЗП» {emojize(":computer:", use_aliases=True)}',
                                      callback_data='show_site'))

    bot.send_message(message.from_user.id, text='Вибери:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('accounting'))
def accounting(call):
    props_keyboard = InlineKeyboardMarkup()
    props_keyboard.add(InlineKeyboardButton(text='Завантажити файл', callback_data='send_props'))

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='<b>Відділ бухгалтерського обліку та звітності, економіки, розподілу асигнувань</b>\n\n'
                               '<b>Приймальня:</b> Оніщенко Ірина Миколаївна\n'
                               '<b>тел.:</b> +380(61)7698368\n\n'
                               f'Щоб отримати платіжні реквізити, натисни {emojize(":point_down:", use_aliases=True)}',
                          reply_markup=props_keyboard, parse_mode='html')
    bot.send_message(chat_id=374464076, text='#asked_accounting')


@bot.callback_query_handler(func=lambda call: call.data.startswith('send_props'))
def send_props(call):
    file_name = 'Платіжні реквізити'
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tmp/'

    doc = open(f'{file_path}{file_name}.docx', 'rb')

    bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    bot.send_document(chat_id=call.from_user.id, data=doc)

    bot.send_message(chat_id=374464076, text='#asked_props')


@bot.callback_query_handler(func=lambda call: call.data.startswith('employment'))
def employment(call):
    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='<b>Центр сприяння працевлаштуванню студентів та випускників</b>\n\n'
                               '<b>Начальник:</b> Ігнашова Анастасія Вікторівна\n'
                               '<b>тел.:</b> +380(61)7698599',
                          parse_mode='html')
    bot.send_message(chat_id=374464076, text='#asked_employment')


@bot.callback_query_handler(func=lambda call: call.data.startswith('profcom'))
def profcom(call):
    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='<b>Профком студентів, аспірантів та докторантів</b>\n\n'
                               '<b>Голова профкому:</b> Іванченко Андрій Володимирович\n'
                               '<b>тел.:</b> +380(61)7698507\n\n'
                               '<b>Заступник голови:</b> Зінченко Марина Михайлівна\n'
                               '<b>тел.:</b> +380(61)7698340',
                          parse_mode='html')
    bot.send_message(chat_id=374464076, text='#asked_profcom')


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_site'))
def show_site(call):
    site_keyboard = InlineKeyboardMarkup()
    site_keyboard.add(InlineKeyboardButton(text='https://zp.edu.ua', url='https://zp.edu.ua'))

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Сайт НУ «ЗП»',
                          reply_markup=site_keyboard)
    bot.send_message(chat_id=374464076, text="#askedwebsite")

