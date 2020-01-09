from db.db import *


class Student(Base):
    __tablename__ = 'student'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    phone = sa.Column(sa.String)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id'))

    group = relationship('Group')

    @staticmethod
    def add_user(id):
        user = Student(id=id)
        session.add(user)

        session.commit()

    @staticmethod
    def update_user(id, name='', phone='', group_id=0):
        user = session.query(Student).get(id)

        if name != '':
            user.name = name
        elif phone != '':
            user.phone = phone
        elif group_id != 0:
            user.group_id = group_id

        session.commit()

    @staticmethod
    def get_user(id):
        return session.query(Student).get(id)


Base.metadata.create_all(conn)
