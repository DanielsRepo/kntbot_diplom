from database.database import *
import random
from sqlalchemy.exc import IntegrityError


class ExtraGrade(Base):
    __tablename__ = 'extragrade'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    extra_grade = sa.Column(sa.Integer)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))

    student = relationship('Student')

    @staticmethod
    def add_extragrade(extra_grade, student_id):
        session.add(ExtraGrade(extra_grade=extra_grade, student_id=student_id))
        session.commit()

    @staticmethod
    def add_extragrades():
        if len(session.query(ExtraGrade).all()) > 0:
            return
        else:
            for student_id in [10, 12, 15, 20, 23, 27, 32, 40, 43, 55, 57]:
                try:
                    session.add(ExtraGrade(extra_grade=random.randint(0, 10), student_id=student_id))
                    session.commit()
                except IntegrityError:
                    continue

            print("extragrades added")

    @staticmethod
    def get_extragrade_by_student(student_id):
        return [grade for grade in session.query(ExtraGrade).filter(ExtraGrade.student_id == student_id)]


Base.metadata.create_all(conn)
