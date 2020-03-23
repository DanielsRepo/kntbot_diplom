from database.database import *
from database.student import Student
from database.group import Group
from database.subject import Subject
import random


class Grade(Base):
    __tablename__ = 'grade'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    grade = sa.Column(sa.Integer)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    subject_id = sa.Column(sa.Integer, sa.ForeignKey('subject.id'))

    student = relationship('Student')
    subject = relationship('Subject')

    @staticmethod
    def add_grade(grade, student_id, subject_id):
        session.add(Grade(grade=grade, student_id=student_id, subject_id=subject_id))
        session.commit()

    @staticmethod
    def add_grades():
        if len(session.query(Grade).all()) > 0:
            return
        else:
            for group in Group.get_groups()[:4]:
                for student in Student.get_students_by_group(group.id):
                    for subject in Subject.get_subjects():
                        session.add(Grade(grade=random.randint(60, 100), student_id=student.id, subject_id=subject.id))
                        session.commit()

            print("grades added")

    @staticmethod
    def get_grades_by_student(student_id):
        return [grade for grade in session.query(Grade).filter(Grade.student_id == student_id)]


Base.metadata.create_all(conn)
