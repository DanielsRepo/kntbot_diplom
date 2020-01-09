from db.db import *


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
    def update_event(id, name='', place='', time='', poster=''):
        event = session.query(Event).get(id)

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
    def get_id_by_name(name):
        event = session.query(Event).filter(Event.name == name).one()
        return event.id

    @staticmethod
    def get_event(id):
        return session.query(Event).get(id)

    @staticmethod
    def get_all_events():
        return session.query(Event).all()

    @staticmethod
    def delete_event(id):
        session.delete(session.query(Event).get(id))
        session.commit()


Base.metadata.create_all(conn)
