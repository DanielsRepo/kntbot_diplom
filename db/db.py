import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

Base = declarative_base()


class Database:
    def __init__(self, admin, password, host, port, database):
        self.admin = admin
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        url = f'postgresql://{self.admin}:{self.password}@{self.host}:{self.port}/{self.database}'
        conn = sa.create_engine(url)
        metadata = sa.MetaData(bind=conn, reflect=True)

        return conn, metadata

    # DEPLOY
    # def __init__(self, admin, password, host, database):
    #     self.admin = admin
    #     self.password = password
    #     self.host = host
    #     self.database = database
    #
    # def connect(self):
    #     url = f'mysql+mysqlconnector://{self.admin}:{self.password}@{self.host}/{self.database}'
    #     conn = sa.create_engine(url)
    #     metadata = sa.MetaData(bind=conn, reflect=True)
    #
    #     return conn, metadata

    @staticmethod
    def delete():
        metadata.drop_all()
        print('deleted')


db = Database('postgres', 'admin', 'localhost', '5432', 'postgres')

conn, metadata = db.connect()
session = Session(conn)
