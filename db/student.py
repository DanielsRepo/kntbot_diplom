from db.db import *

from helpers import students

class Headman(Base):
    __tablename__ = 'headman'

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))

    student = relationship('Student')

    @staticmethod
    def add_headman(headman_id):
        session.add(Headman(student_id=headman_id))
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


class Debtor(Base):
    __tablename__ = 'debtor'

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))

    student = relationship('Student')

    @staticmethod
    def add_debtor(debtor_id):
        session.add(Debtor(student_id=debtor_id))
        session.commit()

    @staticmethod
    def delete_debtor(debtor_id):
        session.delete(session.query(Debtor).filter(Debtor.student_id == debtor_id).one())
        session.commit()

    @staticmethod
    def get_debtors_by_group(group_id):
        debtors = session.query(Debtor, Student).filter(Student.group_id == group_id).filter(Debtor.student_id == Student.id).all()
        print(debtors)
        return [Student.get_student_by_id(debtor[0].student_id).name for debtor in debtors]

    @staticmethod
    def get_all_debtors():
        return [Student.get_student_by_id(debtor.student_id) for debtor in session.query(Debtor).all()]


class Student(Base):
    __tablename__ = 'student'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    phone = sa.Column(sa.String)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id'))

    group = relationship('Group')

    @staticmethod
    def add_students():
        if len(Student.get_all_students()) > 0:
            return
        else:
            group_ids = [1, 2, 3, 4]

            for s in students[:10]:
                session.add(Student(name=s, phone='111111111', group_id=group_ids[0]))

            for s in students[10:25]:
                session.add(Student(name=s, phone='222222222', group_id=group_ids[1]))

            for s in students[25:40]:
                session.add(Student(name=s, phone='333333333', group_id=group_ids[2]))

            for s in students[40:60]:
                session.add(Student(name=s, phone='444444444', group_id=group_ids[3]))

            session.commit()

    @staticmethod
    def add_student(student_id):
        user = Student(id=student_id)
        session.add(user)

        session.commit()

    @staticmethod
    def update_student(student_id, name='', phone='', group_id=0):
        user = session.query(Student).get(student_id)

        if name != '':
            user.name = name
        elif phone != '':
            user.phone = phone
        elif group_id != 0:
            user.group_id = group_id

        session.commit()

    @staticmethod
    def get_student_by_id(student_id):
        return session.query(Student).get(student_id)

    @staticmethod
    def get_students_by_group(group_id):
        return session.query(Student).filter(Student.group_id == group_id)

    @staticmethod
    def get_all_students():
        return [student for student in session.query(Student).all()]


Base.metadata.create_all(conn)
