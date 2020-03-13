from database.database import *
from database.student import Student
from sqlalchemy.orm.exc import NoResultFound


class SubjectDebtor(Base):
    __tablename__ = 'subjectdebtor'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))
    subject_id = sa.Column(sa.Integer, sa.ForeignKey('subject.id'))

    student = relationship('Student')
    subject = relationship('Subject')

    @staticmethod
    def add_debtor(debtor_id, subject_id):
        try:
            # уже есть должник
            if session.query(SubjectDebtor).filter(SubjectDebtor.student_id == debtor_id).filter(SubjectDebtor.subject_id == subject_id).one():
                return False
        except NoResultFound:
            session.add(SubjectDebtor(student_id=debtor_id, subject_id=subject_id))
            session.commit()

        return True

    @staticmethod
    def delete_debtor(debtor_id):
        session.delete(session.query(SubjectDebtor).filter(SubjectDebtor.student_id == debtor_id).one())
        session.commit()

    @staticmethod
    def get_debtors_by_group(group_id):
        debtors = session.query(SubjectDebtor, Student).filter(Student.group_id == group_id).filter(SubjectDebtor.student_id == Student.id).all()
        return [Student.get_student_by_id(debtor[0].student_id) for debtor in debtors]

    @staticmethod
    def get_debtors_by_subject(subject_id):
        return [debtor for debtor in session.query(SubjectDebtor).filter(SubjectDebtor.subject_id == subject_id)]

    @staticmethod
    def get_debt_by_student(student_id):
        return [debt for debt in session.query(SubjectDebtor).filter(SubjectDebtor.student_id == student_id)]


Base.metadata.create_all(conn)
