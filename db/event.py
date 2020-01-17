from db.db import *


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
    time = sa.Column(sa.String)
    poster = sa.Column(sa.String)

    @staticmethod
    def add_event(name):
        event = Event(name=name)
        session.add(event)
        session.commit()
        return event

    @staticmethod
    def update_event(event_id, name='', place='', time='', poster=''):
        event = session.query(Event).get(event_id)
        print(event.name)
        if name != '':
            event.name = name
        elif place != '':
            event.place = place
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
    def get_event_id_by_name(name):
        event = session.query(Event).filter(Event.name == name).one()
        return event.id

    @staticmethod
    def get_event(event_id):
        return session.query(Event).get(event_id)

    @staticmethod
    def get_all_events():
        return [event.name for event in session.query(Event).all()]

    @staticmethod
    def delete_event(event_id):
        session.delete(session.query(EventVisitor).filter(EventVisitor.event_id == event_id).one())
        session.delete(session.query(Event).get(event_id))
        session.commit()


Base.metadata.create_all(conn)
