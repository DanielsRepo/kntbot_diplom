from database.database import *
from database.student import Student
from sqlalchemy.orm.exc import NoResultFound
from database.event import Event
import random


class EventVisitor(Base):
    __tablename__ = 'eventvisitor'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)

    event_id = sa.Column(sa.Integer, sa.ForeignKey('event.id'))
    event = relationship('Event')

    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    student = relationship('Student')

    note = sa.Column(sa.String(256))

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
    def get_all_visitors():
        return [visitor for visitor in session.query(EventVisitor).all()]

    @staticmethod
    def add_visitor(event_id, student_id, note=''):
        event_visit = EventVisitor(event_id=event_id, student_id=student_id, note=note)
        session.add(event_visit)
        session.commit()
        return event_visit

    @staticmethod
    def get_visitors(event_id):
        return [visitor.student_id for visitor in session.query(EventVisitor).filter(EventVisitor.event_id == event_id)]

    @staticmethod
    def get_visitor_by_id(visitor_id):
        return session.query(EventVisitor).filter(EventVisitor.student_id == visitor_id).one()

    @staticmethod
    def check_visitor(event_id, student_id):
        try:
            session.query(EventVisitor).filter(EventVisitor.event_id == event_id). \
                filter(EventVisitor.student_id == student_id).one()
        except NoResultFound:
            return False

    @staticmethod
    def delete_visitor(event_id, student_id):
        session.delete(session.query(EventVisitor).filter(EventVisitor.event_id == event_id).
                       filter(EventVisitor.student_id == student_id).one())
        session.commit()

    @staticmethod
    def get_visitor_students(group_id):
        return session.query(Student, EventVisitor).filter(Student.group_id == group_id).filter(
            EventVisitor.student_id == Student.id).all()


Base.metadata.create_all(conn)
