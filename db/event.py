from db.db import *
from db.student import Student

class EventVisitor(Base):
    __tablename__ = 'eventvisitor'

    id = sa.Column(sa.Integer, primary_key=True)

    event_id = sa.Column(sa.Integer, sa.ForeignKey('event.id'))
    event = relationship('Event')

    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    student = relationship('Student')


class Event(Base):
    __tablename__ = 'event'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    place = sa.Column(sa.String)
    date = sa.Column(sa.String)
    time = sa.Column(sa.String)
    poster = sa.Column(sa.String)

    @staticmethod
    def add_event(name):
        event = Event(name=name)
        session.add(event)
        session.commit()
        return event

    @staticmethod
    def add_events():
        if len(Event.get_all_events()) > 0:
            return
        else:
            session.add(Event(name='Мистер ЗНТУ', place='ауд. 366', date='12.08.20', time='10:00'))
            session.add(Event(name='КВН', place='акт зал', date='20.12.20', time='18:00'))
            session.add(Event(name='Мисс ЗНТУ', place='ауд. 266', date='22.09.20', time='11:00'))
            session.add(Event(name='Ярмарка', place='ауд. 366', date='12.08.20', time='10:00'))
            session.add(Event(name='Бал выпускников', place='ауд. 777', date='12.12.12', time='12:12'))

            session.commit()

    @staticmethod
    def add_visitors():
        for e in Event.get_all_events():
            for s in Student.get_all_students():
                event_visit = EventVisitor(event_id=e.id, student_id=s.id)
                session.add(event_visit)
                session.commit()

    @staticmethod
    def update_event(event_id, name='', place='', date='', time='', poster=''):
        event = session.query(Event).get(event_id)

        if name != '':
            event.name = name
        elif place != '':
            event.place = place
        elif date != '':
            event.date = date
        elif time != '':
            event.time = time
        elif poster != '':
            event.poster = poster

        session.commit()

    @staticmethod
    def add_visitor(event_id, student_id):
        event_visit = EventVisitor(event_id=event_id, student_id=student_id)
        session.add(event_visit)
        session.commit()
        return event_visit

    @staticmethod
    def get_visitors(event_id):
        return [visitor.student_id for visitor in session.query(EventVisitor).filter(EventVisitor.event_id == event_id)]

    @staticmethod
    def get_event_id_by_name(name):
        event = session.query(Event).filter(Event.name == name).one()
        print(event)
        return event.id

    @staticmethod
    def get_event(event_id):
        return session.query(Event).get(event_id)

    @staticmethod
    def get_all_events():
        return [event for event in session.query(Event).all()]

    @staticmethod
    def delete_event(event_id):
        event_visitors = session.query(EventVisitor).filter(EventVisitor.event_id == event_id)

        if len(event_visitors.all()) > 0:
            event_visitors.delete()

        session.delete(session.query(Event).get(event_id))
        session.commit()


Base.metadata.create_all(conn)
