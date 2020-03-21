from database.database import *
from database.student import Student
from sqlalchemy.orm.exc import NoResultFound


class ProfcomDebtor(Base):
    __tablename__ = 'profcomdebtor'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    debt = sa.Column(sa.Integer)

    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))

    student = relationship('Student')

    @staticmethod
    def debtor_exists(debtor_id):
        try:
            if session.query(ProfcomDebtor).filter(ProfcomDebtor.student_id == debtor_id).one():
                return True
        except NoResultFound:
            return False

    @staticmethod
    def get_debt(debtor_id):
        return session.query(ProfcomDebtor).filter(ProfcomDebtor.student_id == debtor_id).one().debt

    @staticmethod
    def add_debtor(debtor_id, debt):
        session.add(ProfcomDebtor(student_id=debtor_id, debt=debt))
        session.commit()

    @staticmethod
    def delete_debtor(debtor_id):
        session.delete(session.query(ProfcomDebtor).filter(ProfcomDebtor.student_id == debtor_id).one())
        session.commit()

    @staticmethod
    def get_debtors_by_group(group_id):
        debtors = session.query(ProfcomDebtor, Student).filter(Student.group_id == group_id).filter(ProfcomDebtor.student_id == Student.id).all()
        return [Student.get_student_by_id(debtor[0].student_id) for debtor in debtors]

    @staticmethod
    def get_all_debtors():
        return [Student.get_student_by_id(debtor.student_id) for debtor in session.query(ProfcomDebtor).all()]


Base.metadata.create_all(conn)
