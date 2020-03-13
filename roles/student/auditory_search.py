from flask import Blueprint
from credentials import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

auditory_search = Blueprint('auditory_search', __name__)


@auditory_search.route('/auditory_search')
def search_aud(message):
    bot.send_message(chat_id=message.from_user.id, text=f'Введи номер потрібної аудиторії')

    bot.register_next_step_handler(message, get_aud)


def get_aud(message):
    if message.text == '/cancel':
        bot.clear_step_handler_by_chat_id(chat_id=message.from_user.id)
        return

    number_query = str(message.text).lower()

    number_query = number_query.replace(' ', '') if ' ' in number_query else number_query
    number_query = number_query.replace('-', '') if '-' in number_query else number_query
    number_query = number_query.replace('\u0061', 'а') if '\u0061' in number_query else number_query

    search_again = InlineKeyboardMarkup()
    search_again.add(InlineKeyboardButton(text=f'{emojize(":mag_right:", use_aliases=True)} Шукати ще',
                                          callback_data='search_aud_again'))

    try:
        number, building, floor = get_aud_from_dict(number_query)

        bot.send_message(chat_id=message.from_user.id,
                         text=f'<b>Аудиторія:</b> {number}\n'
                              f'<b>Корпус:</b> {building}\n'
                              f'<b>Поверх:</b> {floor}',
                         reply_markup=search_again,
                         parse_mode='html')

        bot.send_message(chat_id=374464076, text=f'#found_aud {number}')
    except TypeError:
        bot.send_message(chat_id=message.from_user.id,
                         text=f'Аудиторію не знайдено {emojize(":white_frowning_face:", use_aliases=True)}',
                         reply_markup=search_again)

        bot.send_message(chat_id=374464076, text=f'#no_aud')


def get_aud_from_dict(number):
    auditories_dict = get_auditories_dict()

    for building in auditories_dict:
        for floor in auditories_dict[building]:
            for aud in auditories_dict[building][floor]:
                if aud == str(number):
                    return number, building, floor


@bot.callback_query_handler(func=lambda call: call.data.startswith('search_aud_again'))
def search_aud_again(call):
    message = bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=f'Введи номер потрібної аудиторії')

    bot.register_next_step_handler(message, get_aud)


def get_auditories_dict():
    return {
        '1': {
            '0': ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
            '1': ('125', '125а', '126', '127', '127а', '128', '129', '129а',
                  '131', '132', '133', '134', '135', '136', '137', '138', '139',
                  '140', '141', '142', '142а', '144', '145', '146', '147', '148',
                  '149', '150', '151-1', '151-2', '151-3', '152', '152а', '153',
                  '154', '156', '157', '158', '159', '159а', '160', '160а', '161',
                  '162', '162а', '163', '163в', '164', '164а', '1646', '165', '165а',
                  '166', '166а', '167', '168', '169', '170', '171', '172', '173',
                  '173-1', '174', '174а', '175', '177', '179', '179а', '181',
                  '181а', '182', '183а', '1836'),
            '2': ('214', '214а', '218', '219', '220', '220а', '221', '222', '223',
                  '223а', '224', '226', '226а', '228', '229', '229а', '231', '231а',
                  '232', '233', '234', '235', '236', '237', '238', '239', '240', '241',
                  '242', '243', '244', '245', '246', '247', '248', '249', 'зал періодики',
                  '250', '252', '254', '255', '256', '256а', '257', '257а', '258', '260',
                  '262', '264', '266', '266а', '268', '270', '275', '276', '275а', '277',
                  '277а', '279', '280', '282', '284'),
            '3': ('320', '321', '322', '322а', '323', '323а', '324', '325', '326', '327',
                  '328', '329', '329а', '330', '332', '332а', '333', '334', '335', '336',
                  '337', '338', '338а', '339', '340', '341', '342', '343', '344', '345',
                  '346', '347', '347а', '348', '349', '350', '352', '353', '354а', '354б',
                  '354в', '355', '355а', '355б', '356', '357', '357а', '358', '359', '360',
                  '360а', '361', '362', '363', '365', '365а', '366', '367', '368', '368а',
                  '369', '370', '371', '372', '372а', '373', '374', '375', '376', '377',
                  '378', '379', '379а', '380', '380а', '381', 'музей', 'актовий зал')
        },
        '2': {
            '1': ('102', '104', '105', '106', '107', '108', '110', '112', '115', '117'),
            '2': ('201', '202', '203', '204', '205', '206', '207', '208', '210', '211', '213', '214', '218'),
            '3': ('302', '303', '304', '305', '306', '307', '308', '309', '310', '311', '312', '313', '314', '316')
        },
        '3': {
            '1': ('10', '11', '11а', '12', '13', '14', '15', '15а', '16', '17', '17а', '18', '19'),
            '2': ('20', '21', '21а', '22', '22а', '23', '24', '26', '28', '29'),
            '3': ('30', '31', '32', '32а', '33', '34', '35', '36', '37', '38', '39'),
            '4': ('40', '40а', '41', '42', '43', '44', '45', '46', '47', '48', '49'),
            '5': ('50', '51', '52', '53', '53а', '536', '53в', '54', '55', '56', '57', '58')
        },
        '4': {
            '1': ('185', '185а', '186', '186а', '187', '188', '189', '190', '191',
                  '192', '192а', '193', '194', '196', '196а', '198', '198а', '198б'),
            '2': ('285', '286', '288', '298а', '298б', '299', '289', '290', '290а',
                  '292', '292а', '294', '296', '299'),
            '3': ('385', '386', '386а', '387', '387а', '3876', '388', '389', '390', '390а',
                  '392', '392а', '394', '394а', '396', '398', '398а', '398б'),
            '4': ('483', '485', '485а', '486', '487', '488', '489', '490', '492', '496', '498')
        },
        '5': {
            '0': ('508а',),
            '2': ('520', '521', '522', '523', '523а', '524', '525', '527', '529'),
            '3': ('530', '533', '534', '536', '538', '538а', '539а'),
            '4': ('540', '541', '542', '543', '544', '545', '549а')
        }
    }
