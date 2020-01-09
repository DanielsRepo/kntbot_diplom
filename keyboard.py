from telebot.types import ReplyKeyboardMarkup

buttons = [
    'Расписание звонков',
    'Сайт НУЗП',
    'Поиск аудиторий'
]

keyboard = ReplyKeyboardMarkup(True, True)
keyboard.row(*buttons)