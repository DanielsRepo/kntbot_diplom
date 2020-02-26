from db.db import *
from db.student import Student
from sqlalchemy.orm.exc import NoResultFound


class Debtor(Base):
    __tablename__ = 'debtor'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))

    student = relationship('Student')

    @staticmethod
    def add_debtor(debtor_id):
        try:
            # уже есть должник
            if session.query(Debtor).filter(Debtor.student_id == debtor_id).one():
                return False
        except NoResultFound:
            session.add(Debtor(student_id=debtor_id))
            session.commit()

        return True

    @staticmethod
    def delete_debtor(debtor_id):
        session.delete(session.query(Debtor).filter(Debtor.student_id == debtor_id).one())
        session.commit()

    @staticmethod
    def get_debtors_by_group(group_id):
        debtors = session.query(Debtor, Student).filter(Student.group_id == group_id).filter(Debtor.student_id == Student.id).all()
        return [Student.get_student_by_id(debtor[0].student_id) for debtor in debtors]

    @staticmethod
    def get_all_debtors():
        return [Student.get_student_by_id(debtor.student_id) for debtor in session.query(Debtor).all()]


Base.metadata.create_all(conn)
