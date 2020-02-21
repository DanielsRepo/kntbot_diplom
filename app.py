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
# for starosts


# for dekanat
app.register_blueprint(headman_management)


@app.route("/", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '!', 200


if __name__ == '__main__':
    app.run(debug=True)

# for deploy

# bot.remove_webhook()
# bot.set_webhook(url = f'https://dancher18.pythonanywhere.com/{secret}')
#
# @app.route(f'/{secret}', methods=["POST"])
# def telegram_webhook():
#     if request.headers.get('content-type') == 'application/json':
#         json_string = request.stream.read().decode('utf-8')
#         update = telebot.types.Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return 'ok', 200
#     else:
#         abort(403)

