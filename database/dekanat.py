from database.database import *


class Dekanat(Base):
    __tablename__ = 'dekanat'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    dekanat_id = sa.Column(sa.Integer, unique=True)


Base.metadata.create_all(conn)
