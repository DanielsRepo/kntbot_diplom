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

    @staticmethod
    def delete():
        # for _ in range(50):
        #     print('clean')
        Base.metadata.drop_all(conn)


db = Database('postgres', 'admin', 'localhost', '5432', 'postgres')

conn, metadata = db.connect()
session = Session(conn)

# url = urlparse.urlparse(os.environ['DATABASE_URL'])
# dbname = url.path[1:]
# user = url.username
# password = url.password
# host = url.hostname
# port = url.port

# db = Database(user, password, host, port, dbname)
