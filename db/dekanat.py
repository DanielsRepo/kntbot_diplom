from db.db import *
from db.headman import Headman


class Dekanat(Base):
    __tablename__ = 'Dekanat'

    id = sa.Column(sa.Integer, primary_key=True)

    @staticmethod
    def rate_headman(group_id, sign):
        headman = Headman.get_headman_by_group(group_id)

        if sign == '-':
            headman.rating -= 1
        elif sign == '+':
            headman.rating += 1

        session.commit()
