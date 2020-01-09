from db.db import *


class Group(Base):
    __tablename__ = 'group'

    id = sa.Column(sa.Integer, primary_key=True)
    group = sa.Column(sa.String)

    @staticmethod
    def add_groups():
        group_list = ['116', '126', '216-a', '416', '616', '716']
        for g in group_list:
            group = Group(group=g)
            session.add(group)

        session.commit()

    @staticmethod
    def get_id_by_group(group):
        group = session.query(Group).filter(Group.group == group).one()
        return group.id

    @staticmethod
    def get_group_by_id(group_id):
        group = session.query(Group).get(group_id)
        return group.group

    @staticmethod
    def get_groups():
        return session.query(Group).all()


Base.metadata.create_all(conn)
