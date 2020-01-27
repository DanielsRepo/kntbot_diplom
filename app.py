from flask import Flask, request
from roles.student.registration import registration
from menu import menu
from roles.student.auditory_search import auditory_search
from roles.studdekan.event_organize import event_organize
from roles.student.events import events

from roles.studdekan.headmans import headmans
from roles.studdekan.debtors import debtors

from credentials import *

app = Flask(__name__)

app.register_blueprint(menu)
# for students
app.register_blueprint(registration)
app.register_blueprint(auditory_search)
app.register_blueprint(events)
# for studdekan
app.register_blueprint(event_organize)
app.register_blueprint(headmans)
app.register_blueprint(debtors)
# for starosts


# for dekanat






@app.route("/", methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '!', 200


if __name__ == '__main__':
    app.run(debug=True)

