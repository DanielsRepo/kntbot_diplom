from database.database import *


class Grade(Base):
    __tablename__ = 'grade'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    grade = sa.Column(sa.String(256))
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    subject_id = sa.Column(sa.Integer, sa.ForeignKey('subject.id'))

    student = relationship('Student')
    subject = relationship('Subject')

    @staticmethod
    def add_grade(grade, student_id, subject_id):
        session.add(Grade(grade=grade, student_id=student_id, subject_id=subject_id))
        session.commit()

    @staticmethod
    def get_grade_by_student(student_id):
        return [grade for grade in session.query(Grade).filter(Grade.student_id == student_id)]


Base.metadata.create_all(conn)
