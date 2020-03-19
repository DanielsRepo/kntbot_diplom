from database.database import *


class Cathedra(Base):
    __tablename__ = 'cathedra'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256))
    site = sa.Column(sa.String(256))

    @staticmethod
    def add_cathedras():
        if Cathedra.get_cathedras():
            return
        else:
            cathedras = {'ПЗ': 'https://zp.edu.ua/kafedra-programnih-zasobiv',
                         'САОМ': 'https://zp.edu.ua/kafedra-systemnogo-analizu-ta-obchyslyuvalnoyi-matematyky',
                         'ВМ': 'https://zp.edu.ua/kafedra-vyshchoyi-matematyky',
                         'Ф': 'https://zp.edu.ua/kafedra-fiziki',
                         'ІМ': 'https://zp.edu.ua/kafedra-inozemnih-mov',
                         'УЗЗМП': 'https://zp.edu.ua/kafedra-ukrayinoznavstva-ta-zagalnoyi-movnoyi-pidgotovky',
                         'КСМ': 'https://zp.edu.ua/kafedra-kompyuternih-sistem-ta-merezh-1'
                         }
            for k, v in cathedras.items():
                session.add(Cathedra(name=k, site=v))

            session.commit()

        print("cathedras added")

    @staticmethod
    def get_cathedra_by_id(cathedra_id):
        return session.query(Cathedra).get(cathedra_id)

    @staticmethod
    def get_cathedras():
        return [cathedra for cathedra in session.query(Cathedra).all()]


Base.metadata.create_all(conn)
