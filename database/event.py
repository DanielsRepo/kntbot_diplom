from database.database import *
import random
from database.event_visitor import EventVisitor


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256))
    place = sa.Column(sa.String(256))
    date = sa.Column(sa.String(256))
    time = sa.Column(sa.String(256))
    over = sa.Column(sa.Boolean)

    @staticmethod
    def add_event(name):
        event = Event(name=name)
        session.add(event)
        session.commit()
        return event

    @staticmethod
    def add_events():
        if len(Event.get_all_events()) > 0:
            return True
        else:
            session.add(Event(name='Мистер ЗНТУ', place='ауд. 366', date='12.08.20', time='10:00', over=False))
            session.add(Event(name='КВН', place='акт зал', date='20.12.20', time='18:00', over=False))
            session.add(Event(name='Мисс ЗНТУ', place='ауд. 266', date='22.09.20', time='11:00', over=False))
            session.add(Event(name='Бал выпускников', place='ауд. 777', date='12.12.12', time='12:12', over=False))

            session.commit()

        print("events added")

    @staticmethod
    def add_visitors():
        if len(EventVisitor.get_all_visitors()) > 0:
            return
        else:
            for event in Event.get_all_events():
                s_id_list = random.sample(range(1, 61), random.randint(20, 40))
                for s_id in s_id_list:
                    event_visit = EventVisitor(event_id=event.id, student_id=s_id)
                    session.add(event_visit)

                session.commit()

        print("visitors added")

    @staticmethod
    def update_event(event_id, name='', place='', date='', time='', over=''):
        event = session.query(Event).get(event_id)

        if name != '':
            event.name = name
        elif place != '':
            event.place = place
        elif date != '':
            event.date = date
        elif time != '':
            event.time = time
        elif over != '':
            event.over = over

        session.commit()

    @staticmethod
    def get_event_id_by_name(name):
        event = session.query(Event).filter(Event.name == name).one()
        return event.id

    @staticmethod
    def get_event(event_id):
        return session.query(Event).get(event_id)

    @staticmethod
    def get_all_events():
        return [event for event in session.query(Event).all() if event.over is False]

    @staticmethod
    def delete_event(event_id):
        event = Event.get_event(event_id)
        event.over = True
        # event_visitors = session.query(EventVisitor).filter(EventVisitor.event_id == event_id)
        #
        # if len(event_visitors.all()) > 0:
        #     event_visitors.delete()
        #
        # session.delete(session.query(Event).get(event_id))
        session.commit()


Base.metadata.create_all(conn)
