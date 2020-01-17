from db.db import *


class Headman(Base):
    __tablename__ = 'headman'

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))

    student = relationship('Student')

    @staticmethod
    def add_headman(headman_id):
        session.add_headman(Headman(student_id=headman_id))
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
    def get_all_debtors():
        for debtor in session.query(Debtor).all()
            session.query(Debtor).filter(Debtor.student_id == debtor_id)

        Student.get_student_by_id(Debtor.)

        return [debtor.name for debtor in session.query(Debtor).all()]
        

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
            print(len(Student.get_all_students()))
            return
        else:
            group_ids = [1, 2]

            session.add(Student(name=f'Цветков Флор Ярославович', phone='21323523', group_id=group_ids[0]))
            session.add(Student(name=f'Селезнёв Мартин Альбертович', phone='325634', group_id=group_ids[0]))
            session.add(Student(name=f'Ковалёв Бронислав Игоревич', phone='456547', group_id=group_ids[0]))
            session.add(Student(name=f'Назаров Гурий Адольфович', phone='2345231', group_id=group_ids[0]))
            session.add(Student(name=f'Белов Ян Созонович', phone='2345231', group_id=group_ids[0]))

            session.add(Student(name=f'Овчинников Корнелий Вадимович', phone='21323523', group_id=group_ids[1]))
            session.add(Student(name=f'Фомичёв Феликс Григорьевич', phone='325634', group_id=group_ids[1]))
            session.add(Student(name=f'Князев Модест Мэлорович', phone='456547', group_id=group_ids[1]))
            session.add(Student(name=f'Козлов Иван Федорович', phone='2345231', group_id=group_ids[1]))
            session.add(Student(name=f'Фёдоров Альберт Германнович', phone='2345231', group_id=group_ids[1]))

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
        return [student.name for student in session.query(Student).all()]


Base.metadata.create_all(conn)
