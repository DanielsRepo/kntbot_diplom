from db.db import *
import random
from sqlalchemy.orm.exc import NoResultFound


class Audience(Base):
    __tablename__ = 'audience'

    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.String(16))
    building_id = sa.Column(sa.Integer, sa.ForeignKey('building.id'))
    floor_id = sa.Column(sa.Integer, sa.ForeignKey('floor.id'))

    building = relationship('Building')
    floor = relationship('Floor')

    @staticmethod
    def add_aud():
        if len(Audience.get_all_aud()) > 0:
            return
        else:
            buildings_list = [1, 2, 3, 4, 5]
            for n in buildings_list:
                session.add(Building(number=n))

            floors_list = [1, 2, 3, 4, 5]
            for n in floors_list:
                session.add(Floor(number=n))

            aud_list = [random.randint(100, 300) for _ in range(30)]
            for i in aud_list:
                aud = Audience(number=i, building_id=random.randint(1, 4), floor_id=random.randint(1, 4))
                session.add(aud)

        session.commit()

    @staticmethod
    def get_aud(number):
        try:
            aud = session.query(Audience).filter(Audience.number == number).one()
            building = session.query(Building).get(aud.building_id)
            floor = session.query(Floor).get(aud.floor_id)

            return building.number, floor.number

        except NoResultFound:
            return None

    @staticmethod
    def get_all_aud():
        return session.query(Audience).all()


class Building(Base):
    __tablename__ = 'building'

    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.Integer)


class Floor(Base):
    __tablename__ = 'floor'

    id = sa.Column(sa.Integer, primary_key=True)
    number = sa.Column(sa.Integer)


Base.metadata.create_all(conn)
