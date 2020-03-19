from flask import Blueprint
from credentials import bot
from database.headman import Headman
from database.group import Group
from database.student import Student
from keyboards.keyboard import make_keyboard, make_headman_rate_keyboard, make_role_replykeyboard, dekanat_buttons
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

rating_formation = Blueprint('rating_formation', __name__)


@rating_formation.route('/rating_formation')
@bot.callback_query_handler(func=lambda call: call.data.startswith('create_rating'))
def create_rating(message):
    bot.send_message(chat_id=message.from_user.id, text='rating_formation')
