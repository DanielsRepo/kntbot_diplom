from db.db import *


class Group(Base):
    __tablename__ = 'group'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)

    @staticmethod
    def add_groups():
        if len(Group.get_groups()) > 0:
            return
        else:
            group_list = [str(i+1) for i in range(61)]
            for g in group_list:
                group = Group(name=g)
                session.add(group)

            session.commit()

    @staticmethod
    def get_id_by_group(group):
        group = session.query(Group).filter(Group.name == group).one()
        return group.id

    @staticmethod
    def get_group_by_id(group_id):
        group = session.query(Group).get(group_id)
        return group.name

    @staticmethod
    def get_groups():
        return [group.name for group in session.query(Group).all()]


Base.metadata.create_all(conn)
