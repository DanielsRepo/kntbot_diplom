from flask import Blueprint
from credentials import bot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
from keyboards.keyboard import make_keyboard
from database.teacher import Teacher
from database.cathedra import Cathedra


teachers = Blueprint('teachers', __name__)


@teachers.route('/teachers')
def teacher_keyboard(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'Розклад викладачів {emojize(":clipboard:", use_aliases=True)}',
                                      callback_data='teachers_schelude'))
    keyboard.add(InlineKeyboardButton(text=f'Контактна інформація {emojize(":e-mail:", use_aliases=True)}',
                                      callback_data='teachers_info'))

    bot.send_message(message.from_user.id, text='Вибери:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('teachers_schelude'))
def teachers_schelude(call):
    file_name = 'Розклад викладачів'
    file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tmp/'

    doc = open(f'{file_path}{file_name}.xls', 'rb')

    bot.send_document(chat_id=call.from_user.id, data=doc)

    # bot.send_message(chat_id=374464076, text='#asked_teachers')


@bot.callback_query_handler(func=lambda call: call.data.startswith('teachers_info'))
def choose_cathedra(message):
    cathedra_keyboard = make_keyboard(keyboard_type='cathedra',
                                      elem_list=Cathedra.get_cathedras(),
                                      marker='teachercathedra_')

    bot.edit_message_text(chat_id=message.from_user.id,
                          message_id=message.message.message_id,
                          text='Вибери кафедру:',
                          reply_markup=cathedra_keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('teachercathedra_'))
def get_cathedra_info(call):
    cathedra_id = call.data.split('_')[1]
    cathedra = Cathedra.get_cathedra_by_id(cathedra_id)

    # bot.send_message(chat_id=374464076, text=f'#asked_cathedra {cathedra.name}')

    teachers_button = InlineKeyboardMarkup()
    message_text = ''

    if cathedra_id == '1':
        message_text = f'<b><a href="{cathedra.site}">Кафедра програмних засобів</a></b>\n\n' \
                       '<b>кабінет:</b> 43 \n' \
                       '<b>тел.:</b> +380(61)7698267\n' \
                       '<b>e-mail:</b> kafedra_pz@zntu.edu.ua\n\n' \
                       '<b>Завідувач кафедри</b>\n' \
                       '<a href="https://zp.edu.ua/sergiy-oleksandrovich-subbotin">' \
                       'Субботін Сергій Олександрович</a>\n\n' \
                       '<b>тел.:</b> +380(61)7646330\n' \
                       '<b>e-mail:</b> subbotin.csit@gmail.com'

        teachers_button.add(InlineKeyboardButton(text='Викладачі кафедри', callback_data=f'teachersinfo_{cathedra_id}'))
    elif cathedra_id == '2':
        message_text = f'<b><a href="{cathedra.site}">' \
                       f'Кафедра системного аналізу та обчислювальної математики</a></b>\n\n' \
                       '<b>кабінет:</b> 361\n' \
                       '<b>тел.:</b> +380(61)7698267\n' \
                       '<b>e-mail:</b> kafedra_pz@zntu.edu.ua\n\n' \
                       '<b>Завідувач кафедри</b>\n' \
                       '<a href="https://zp.edu.ua/?q=node/3110">Корніч Григорій Володимирович</a>\n\n' \
                       '<b>кабінет:</b> 361, 231a\n' \
                       '<b>тел.:</b> +380(61)7698247\n' \
                       '<b>e-mail:</b> gkornich@zntu.edu.ua'

        teachers_button.add(InlineKeyboardButton(text='Викладачі кафедри', callback_data=f'teachersinfo_{cathedra_id}'))
    elif cathedra_id == '3':
        message_text = f'<b><a href="{cathedra.site}">' \
                       f'Кафедра вищої математики</a></b>\n\n' \
                       '<b>кабінет:</b> 216\n' \
                       '<b>тел.:</b> +380(61)7698446\n' \
                       '<b>e-mail:</b> kafedra_vm@zntu.edu.ua\n\n' \
                       '<b>Завідувач кафедри</b>\n' \
                       '<a href="https://zp.edu.ua/?q=node/3450">Володимир Михайлович Онуфрієнко</a>\n\n' \
                       '<b>кабінет:</b> 201\n' \
                       '<b>тел.:</b>  +380(61)7646575; +380(61)7698487\n'

        teachers_button.add(InlineKeyboardButton(text='Викладачі кафедри',
                            url='https://zp.edu.ua/spisok-spivrobitnikiv-kafedri-vishchoyi-matematiki'))
    elif cathedra_id == '4':
        message_text = f'<b><a href="{cathedra.site}">' \
                       f'Кафедра фізики</a></b>\n\n' \
                       '<b>кабінет:</b> 328\n' \
                       '<b>тел.:</b> +380(61)7698490\n' \
                       '<b>e-mail:</b> kafedra_fizika@zntu.edu.ua\n\n' \
                       '<b>Завідувач кафедри</b>\n' \
                       '<a href="https://zp.edu.ua/?q=node/622">Степан Васильович Лоскутов</a>\n\n' \
                       '<b>кабінет:</b> 324\n' \
                       '<b>тел.:</b> +38(061)7698355\n' \
                       '<b>e-mail:</b> svl@zntu.edu.ua'

        teachers_button.add(InlineKeyboardButton(text='Викладачі кафедри',
                            url='https://zp.edu.ua/vikladachi-ta-spivrobitniki-kafedri-fizika'))
    elif cathedra_id == '5':
        message_text = f'<b><a href="{cathedra.site}">' \
                       f'Кафедра іноземних мов</a></b>\n\n' \
                       '<b>кабінет:</b> 348\n' \
                       '<b>тел.:</b> +380(61)7698248\n' \
                       '<b>e-mail:</b> kafedra_in_mov@zntu.edu.ua\n\n' \
                       '<b>Завідувач кафедри</b>\n' \
                       '<a href="https://zp.edu.ua/?q=node/622">Соболь Юлія Олександрівна</a>\n\n' \
                       '<b>кабінет:</b> 330-Б\n' \
                       '<b>тел.:</b> +380(61)7698522\n' \
                       '<b>e-mail:</b> sobolyuliya@gmail.com'

        teachers_button.add(InlineKeyboardButton(text='Викладачі кафедри',
                            url='https://zp.edu.ua/vykladachi-ta-spivrobitnyky-kafedry-inozemnyh-mov'))
    elif cathedra_id == '6':
        message_text = f'<b><a href="{cathedra.site}">' \
                       f'Кафедра українознавства та загальної мовної підготовки</a></b>\n\n' \
                       '<b>кабінет:</b> 269\n' \
                       '<b>тел.:</b> +38(061)7642314\n' \
                       '<b>e-mail:</b> kafedra_ukr_zn@zntu.edu.ua\n\n' \
                       '<b>Завідувач кафедри</b>\n' \
                       '<a href="https://zp.edu.ua/?q=node/1190">Шаповалов Георгій Іванович</a>\n\n' \
                       '<b>кабінет:</b> 270\n' \
                       '<b>тел.:</b> +38(061)7698336; +38(061)7698375\n' \
                       '<b>e-mail:</b> jakirhrest@gmail.com'
    elif cathedra_id == '7':
        message_text = f'<b><a href="{cathedra.site}">' \
                       f"Кафедра комп'ютерних систем та мереж</a></b>\n\n" \
                       '<b>кабінет:</b> 53-Б\n' \
                       '<b>тел.:</b> +380(61)698249\n' \
                       '<b>e-mail:</b> kafedra_ksm@zntu.edu.ua\n\n'\
                       '<b>Завідувач кафедри</b>\n' \
                       '<a href="https://zp.edu.ua/?q=node/2726">Равіль Камілович Кудерметов</a>\n\n' \
                       '<b>кабінет:</b> 53-Б\n' \
                       '<b>тел.:</b> +380(61)698249\n'

        teachers_button.add(InlineKeyboardButton(text='Викладачі кафедри',
                            url='https://zp.edu.ua/vikladachi-ta-spivrobitniki-kafedri-ksm'))

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=message_text,
                          reply_markup=teachers_button,
                          parse_mode='html', disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('teachersinfo_'))
def choose_teacher(call):
    cathedra_id = call.data.split('_')[1]

    teachers_info_keyboard = make_keyboard(keyboard_type='teacher',
                                           elem_list=Teacher.get_teachers_by_cathedra(cathedra_id),
                                           marker='showteacher_')

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text='Викладачі кафедри',
                          reply_markup=teachers_info_keyboard,
                          parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('showteacher_'))
def get_teacher_info(call):
    teacher_id = call.data.split('_')[1]
    teacher = Teacher.get_teacher_by_id(teacher_id)

    message_text = f'<b><a href="{teacher.site}">' \
                   f'{teacher.name}</a></b>\n\n' \
                   f'<b>e-mail:</b> {teacher.email}\n' \

    bot.edit_message_text(chat_id=call.from_user.id,
                          message_id=call.message.message_id,
                          text=message_text,
                          parse_mode='html', disable_web_page_preview=True)
    # bot.send_message(chat_id=374464076, text=f'#asked_teacher {teacher.name}')


