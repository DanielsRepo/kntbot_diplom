from database.database import *
from database.student import Student
from database.group import Group
from database.subject import Subject
from datetime import date
import random


class Grade(Base):
    __tablename__ = 'grade'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    grade = sa.Column(sa.Integer)
    ects = sa.Column(sa.String(256))

    date = sa.Column(sa.String(256))

    gradetype_id = sa.Column(sa.Integer, sa.ForeignKey('gradetype.id'))
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    subject_id = sa.Column(sa.Integer, sa.ForeignKey('subject.id'))

    gradetype = relationship('GradeType')
    student = relationship('Student')
    subject = relationship('Subject')

    @staticmethod
    def add_grade(grade, gradetype_id, student_id, subject_id):
        session.add(Grade(grade=grade,
                          ects=Grade.convert_to_ects(int(grade)),
                          date=date.today().strftime("%d/%m/%Y"),
                          gradetype_id=gradetype_id,
                          student_id=student_id,
                          subject_id=subject_id))
        session.commit()

    @staticmethod
    def convert_to_ects(grade):
        if grade >= 90:
            return 'A'
        elif grade >= 85:
            return 'B'
        elif grade >= 75:
            return 'C'
        elif grade >= 60:
            return 'D'
        else:
            return 'F'

    @staticmethod
    def add_grades():
        if len(session.query(Grade).all()) > 0:
            return
        else:
            for group in Group.get_groups()[:4]:
                for student in Student.get_students_by_group(group.id):
                    for subject in Subject.get_subjects():
                        grade = random.randint(60, 100)
                        gradetype_id = random.randint(1, 5)
                        session.add(Grade(grade=grade,
                                          ects=Grade.convert_to_ects(grade),
                                          date=date.today().strftime("%m/%d/%Y"),
                                          gradetype_id=gradetype_id,
                                          student_id=student.id,
                                          subject_id=subject.id))
                        session.commit()

            print("grades added")

    @staticmethod
    def get_grades_by_student(student_id):
        return [grade for grade in session.query(Grade).filter(Grade.student_id == student_id)]


Base.metadata.create_all(conn)
