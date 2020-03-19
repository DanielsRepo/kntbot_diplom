from database.database import *


class Teacher(Base):
    __tablename__ = 'teacher'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256))
    email = sa.Column(sa.String(256))
    site = sa.Column(sa.String(256))
    cathedra_id = sa.Column(sa.Integer, sa.ForeignKey('cathedra.id'))

    cathedra = relationship('Cathedra')

    @staticmethod
    def add_teachers():
        if session.query(Teacher).all():
            return
        else:
            for name, contacts in pz_teachers.items():
                session.add(Teacher(name=name, email=contacts[0], site=contacts[1], cathedra_id=1))

            for name, contacts in saom_teachers.items():
                session.add(Teacher(name=name, email=contacts[0], site=contacts[1], cathedra_id=2))

            session.commit()

            print("teachers added")

    @staticmethod
    def get_teacher_by_id(teacher_id):
        return session.query(Teacher).get(teacher_id)

    @staticmethod
    def get_teachers_by_cathedra(cathedra_id):
        return session.query(Teacher).filter(Teacher.cathedra_id == cathedra_id).all()


Base.metadata.create_all(conn)

saom_teachers = {
    'Корніч Григорій Володимирович': [
        'gvkornich@gmail.com',
        'https://zp.edu.ua/?q=node/3110'
    ],
    'Бакурова Анна Володимирівна': [
        'abaka111060@gmail.com',
        'https://zp.edu.ua/anna-volodymyrivna-bakurova'
    ],
    'Бахрушин Володимир Євгенович': [
        'vladimir.bakhrushin@gmail.com',
        'https://zp.edu.ua/?q=node/5005'
    ],
    'Денисенко Олександр Іванович': [
        'alexdem345@gmail.com',
        'https://zp.edu.ua/?q=node/2670'
    ],
    'Пархоменко Лариса Олександрівна': [
        'dilap@zntu.edu.ua',
        'https://zp.edu.ua/?q=node/3020'
    ],
    'Подковаліхіна Олена Олександрівна': [
        'epodkovalihina@gmail.com',
        'https://zp.edu.ua/podkovalihina-olena-oleksandrivna',
    ],
    'Рябенко Антон Євгенович': [
        'rjabenkoae@gmail.com',
        'https://zp.edu.ua/?q=node/2730'
    ],
    'Савранська Алла Володимирівна': [
        'savranskaya-alla@ukr.net',
        '-'
    ],
    'Терещенко Еліна Валентинівна': [
        'elina_vt@ukr.net',
        'https://zp.edu.ua/?q=node/2672'
    ],
    'Кривцун Олена Володимирівна': [
        'kryvtsun@ukr.net',
        'https://zp.edu.ua/olena-volodymyrivna-kryvcun'
    ],
    'Широкорад Дмитро Вікторович': [
        'hoveringphoenix@gmail.com',
        'https://zp.edu.ua/?q=node/7785'
    ]
}

pz_teachers = {
    'Субботін Сергій Олександрович': [
        'subbotin.csit@gmail.com',
        'https://zp.edu.ua/sergiy-oleksandrovich-subbotin'
    ],
    'Дубровін Валерій Іванович': [
        'vdubrovin@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/657'
    ],
    'Табунщик Галина Володимирівна': [
        'galina.tabunshchik@gmail.com',
        'https://zp.edu.ua/galina-volodimirivna-tabunshchik'
    ],
    'Корнієнко Сергій Костянтинович': [
        'kornienko.zntu@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/659'
    ],
    'Олійник Андрій Олександрович': [
        'olejnikaa@gmail.com',
        'https://zp.edu.ua/andriy-oleksandrovich-oliynik'
    ],
    'Пархоменко Анжеліка Володимирівна': [
        'parhom@zntu.edu.ua',
        'https://zp.edu.ua/anzhelika-volodimirivna-parhomenko'
    ],
    'Сердюк Сергій Микитович': [
        'serdjuksn@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/663'
    ],
    'Степаненко Олександр Олексійович': [
        'alex@zntu.edu.ua',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/668'
    ],
    'Федорончак Тетяна Василівна': [
        't.fedoronchak@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/679'
    ],
    'Зайко Тетяна Анатоліївна': [
        '-',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/6868'
    ],
    'Каплієнко Тетяна Ігорівна': [
        '-',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/686'
    ],
    'Колпакова Тетяна Олексіївна': [
        't.o.kolpakova@gmail.com',
        'https://zp.edu.ua/tetyana-oleksiyivna-kolpakova'
    ],
    'Льовкін Валерій Миколайович': [
        'vliovkin@gmail.com',
        'https://zp.edu.ua/valeriy-mikolayovich-lovkin'
    ],
    'Миронова Наталя Олексіївна': [
        'natali.myronova@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/676'
    ],
    'Дейнега Лариса Юріївна': [
        'deynega.larisa@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/673'
    ],
    'Качан Олександр Іванович': [
        'alexander.j.katschan@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/675'
    ],
    'Левада Ірина Василівна': [
        'peklev@rambler.ru',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/671'
    ],
    'Федорченко Євген Миколайович': [
        'evg.fedorchenko@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/678'
    ],
    'Камінська Жанна Костянтинівна': [
        'kamzhana@gmail.com',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/674'
    ],
    'Скачко Лілія Павлівна': [
        '-',
        'https://zp.edu.ua/kafedra-programnih-zasobiv?q=node/677'
    ],
    'Неласа Ганна Вікторівна': [
        'annanelasa@gmail.com',
        'https://zp.edu.ua/kafedra-zahistu-informaciyi?q=node/1382'
    ],
    'Андреєв Максим Олександрович': [
        'chabb.zntu@gmail.com',
        'https://zp.edu.ua/?q=node/688'
    ],
    'Калініна Марина Володимирівна': [
        '-',
        'https://zp.edu.ua/universitet/kafedra-programnih-zasobiv?q=node/687'
    ],
    'Туленков Артем Вікторович': [
        'aetulenkov@gmail.com',
        '-'
    ]
}
