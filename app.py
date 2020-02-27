from flask import Flask, request
from roles.student.registration import registration
from menu import menu
from roles.student.auditory_search import auditory_search
from roles.student.teachers import teachers
from roles.studdekan.event_organize import event_organize
from roles.studdekan.event_visits import event_visits
from roles.student.events import events
from roles.studdekan.headmans import headmans
from roles.studdekan.debtors import debtors
from roles.dekanat.headman_management import headman_management
from credentials import bot, secret, telebot
from db.db import session

app = Flask(__name__)

app.register_blueprint(menu)
# for students
app.register_blueprint(registration)
app.register_blueprint(auditory_search)
app.register_blueprint(events)
app.register_blueprint(teachers)
# for studdekan
app.register_blueprint(event_organize)
app.register_blueprint(event_visits)
app.register_blueprint(headmans)
app.register_blueprint(debtors)
# for dekanat
app.register_blueprint(headman_management)


@app.teardown_appcontext
def shutdown_session(exception=None):
    print('session close')
    session.close()


@app.route("/", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '!', 200

# DEPLOY
# @app.route(f'/{secret}', methods=["POST"])
# def telegram_webhook():
#     updates = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
#
#     try:
#         bot.process_new_updates([updates])
#     except BaseException as e:
#         print('BaseException OperationalError handled, session close')
#         bot.send_message(374464076, text=f'BaseException handled :D \n\n {str(e)}')
#
#         bot.process_new_updates([updates])
#
#     return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)


