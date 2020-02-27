from db.db import *
from sqlalchemy.exc import ProgrammingError
from db.group import Group


class Student(Base):
    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(256))
    name = sa.Column(sa.String(256))
    phone = sa.Column(sa.String(256))
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id'))

    group = relationship('Group')

    @staticmethod
    def add_students():
        if len(Student.get_all_students()) > 0:
            return True
        else:
            group_ids = [1, 2, 3, 4]

            for s in students[:10]:
                session.add(Student(name=s, username='dfherher4', phone='111111111', group_id=group_ids[0]))

            for s in students[10:25]:
                session.add(Student(name=s, username='rethrhtr', phone='222222222', group_id=group_ids[1]))

            for s in students[25:40]:
                session.add(Student(name=s, username='erherrher', phone='333333333', group_id=group_ids[2]))

            for s in students[40:60]:
                session.add(Student(name=s, username='erherhr', phone='444444444', group_id=group_ids[3]))

            session.commit()

            print("students added")

    @staticmethod
    def add_student(student_id, student_username):
        user = Student(id=student_id, username=student_username)
        session.add(user)

        session.commit()

    @staticmethod
    def update_student(student_id, name='', phone='', group_id=0):
        user = session.query(Student).get(student_id)

        if name != '':
            user.name = name
        elif phone != '':
            user.phone = phone
        elif group_id != 0:
            user.group_id = group_id

        session.commit()

        return user

    @staticmethod
    def get_student_by_id(student_id):
        try:
            return session.query(Student).get(student_id)
        except ProgrammingError:
            return None

    @staticmethod
    def get_students_by_group(group_id):
        return session.query(Student).filter(Student.group_id == group_id)

    @staticmethod
    def get_all_students():
        return [student for student in session.query(Student).all()]

    @staticmethod
    def check_fac(student_id):
        if Student.get_student_by_id(student_id).group_id != Group.get_id_by_group('other'):
            return True


Base.metadata.create_all(conn)


students = [
    'Костин Юстин Леонидович',
    'Яковлев Ефрем Якунович',
    'Исаев Мирослав Сергеевич',
    'Николаев Флор Игоревич',
    'Федотов Агафон Богуславович',
    'Артемьев Тимур Филатович',
    'Белозёров Май Игоревич',
    'Денисов Тарас Лукьевич',
    'Беляков Мартин Вадимович',
    'Мамонтов Всеволод Сергеевич',
    'Миронов Геннадий Улебович',
    'Симонов Арсений Георгиевич',
    'Соловьёв Юстин Романович',
    'Трофимов Феликс Альвианович',
    'Михеев Глеб Викторович',
    'Гордеев Азарий Геннадьевич',
    'Молчанов Мечеслав Федотович',
    'Сергеев Корнелий Валерьянович',
    'Поляков Авраам Авдеевич',
    'Пономарёв Богдан Викторович',
    'Горшков Варлам Куприянович',
    'Колесников Эрик Богданович',
    'Лаврентьев Гордий Платонович',
    'Богданов Владимир Донатович',
    'Савельев Нелли Денисович',
    'Наумов Витольд Александрович',
    'Гришин Лукьян Богданович',
    'Мясников Семен Иосифович',
    'Котов Лев Аркадьевич',
    'Шарапов Мирон Егорович',
    'Мартынов Устин Викторович',
    'Денисов Панкратий Владиславович',
    'Авдеев Герасим Богуславович',
    'Степанов Игнатий Иванович',
    'Третьяков Аполлон Павлович',
    'Суханов Степан Тимофеевич',
    'Агафонов Касьян Никитевич',
    'Евсеев Терентий Рудольфович',
    'Шаров Устин Яковлевич',
    'Белозёров Мартин Павлович',
    'Лапин Альфред Антонович',
    'Громов Иван Яковлевич',
    'Павлов Ефрем Юлианович',
    'Пономарёв Карл Борисович',
    'Наумов Филипп Арсеньевич',
    'Лобанов Гордий Артемович',
    'Тимофеев Георгий Валерьянович',
    'Петров Гаянэ Владиславович',
    'Овчинников Юлий Авксентьевич',
    'Беспалов Велор Рудольфович',
    'Субботин Аскольд Мартынович',
    'Савин Максим Антонович',
    'Давыдов Станислав Дмитриевич',
    'Тарасов Алексей Александрович',
    'Иванков Ефрем Богданович',
    'Самойлов Евгений Эльдарович',
    'Осипов Эльдар Фролович',
    'Панов Аркадий Константинович',
    'Логинов Флор Валерьянович',
    'Копылов Рубен Протасьевич',
]
