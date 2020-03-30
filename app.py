from flask import Flask, request
from roles.student.registration import registration
from keyboards.menu import menu
from roles.student.auditory_search import auditory_search
from roles.student.teachers import teachers
from roles.student.univer_info import univer_info
from roles.student.studying import studying
from roles.studdekan.event_organization import event_organize
from roles.studdekan.getting_eventvisits import event_visits
from roles.studdekan.extragrade_assignment import extragrade_assignment

from roles.student.events_schelude import events
from roles.studdekan.headman_management import headmans
from roles.studdekan.profcomdebtor_management import debtors
from roles.dekanat.headman_communication import headman_management
from roles.dekanat.rating_formation import rating_formation

from roles.teacher.student_communication import student_communication
from roles.teacher.subjectdebtor_management import subject_debtors
from roles.teacher.grade_assignment import grades
from credentials import bot, telebot
from database.database import session

app = Flask(__name__)

app.register_blueprint(menu)
# for students
app.register_blueprint(registration)
app.register_blueprint(auditory_search)
app.register_blueprint(events)
app.register_blueprint(teachers)
app.register_blueprint(studying)
app.register_blueprint(univer_info)
# for studdekan
app.register_blueprint(event_organize)
app.register_blueprint(event_visits)
app.register_blueprint(headmans)
app.register_blueprint(debtors)
app.register_blueprint(extragrade_assignment)
# for dekanat
app.register_blueprint(headman_management)
app.register_blueprint(rating_formation)
# for teacher
app.register_blueprint(subject_debtors)
app.register_blueprint(student_communication)
app.register_blueprint(grades)


@app.teardown_appcontext
def shutdown_session(exception=None):
    print('session close')
    session.close()


@app.route("/", methods=['POST'])
def webhook():
    try:
        bot.process_new_updates([telebot.types.Update.de_json
                                 (request.stream.read().
                                  decode("utf-8"))])
    except BaseException as e:
        print('BaseException OperationalError handled, session close')
        bot.send_message(374464076, text=f'BaseException handled :D \n\n {str(e)}')

        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])

    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)
