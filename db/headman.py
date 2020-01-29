from db.db import *
from db.student import Student


class Headman(Base):
    __tablename__ = 'headman'

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    rating = sa.Column(sa.Integer)

    student = relationship('Student')

    @staticmethod
    def add_headman(headman_id):
        session.add(Headman(student_id=headman_id, rating=6))
        session.commit()

    @staticmethod
    def get_headman_by_group(group_id):
        return session.query(Headman, Student).filter(Student.group_id == group_id).filter(Headman.student_id == Student.id).scalar()

    @staticmethod
    def change_headman(new_headman_id):
        new_headman = Student.get_student_by_id(new_headman_id)
        old_headman = Headman.get_headman_by_group(new_headman.group_id)
        old_headman.student_id = new_headman.id
        session.commit()

    @staticmethod
    def get_all_headmans():
        return [headman.student_id for headman in session.query(Headman).all()]
