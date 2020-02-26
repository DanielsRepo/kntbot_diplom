from db.db import *
from sqlalchemy.orm.exc import NoResultFound


class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(32))

    @staticmethod
    def add_groups():
        if len(Group.get_groups()) > 0:
            return True
        else:
            # group_list = [str(i+1) for i in range(61)]
            group_list = [
                '119', '129', '139', '119сп', '129сп', '219', '229', '219сп', '519', '519сп', '819', '819сп', '118',
                '128', '138', '218', '518', '528', '228', '128сп', '228сп', '118сп', '518сп', '818', '818сп', '117',
                '127', '137', '237сп', '217', '227', '517', '527', '817', '827сп', '218сп', '537сп', '147сп', '116',
                '157сп', '126', '216', '516', '526', '816', '226', '129м', '219м', '819м', '119м', '519м', 'other'
            ]
            for g in group_list:
                group = Group(name=g)
                session.add(group)

            session.commit()

        print("groups added")

    @staticmethod
    def get_id_by_group(group):
        try:
            group = session.query(Group).filter(Group.name == group).one()
            return group.id
        except NoResultFound:
            return False

    @staticmethod
    def get_group_by_id(group_id):
        group = session.query(Group).get(group_id)
        return group.name

    @staticmethod
    def get_groups():
        return [group for group in session.query(Group).all()]


Base.metadata.create_all(conn)
