from database.database import *


class Subject(Base):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256))
    fullname = sa.Column(sa.String(256))

    @staticmethod
    def add_subjects():
        subjects = [("Об'єктно орієнтоване програмування", 'ООП'),
                    ('Основи програмної інжеренії', 'ОПІ'),
                    ('Аналіз вимог до програмного забезпечення', 'АВдоПЗ'),
                    ('Групова динаміка і комунікації', 'ГДіК'),
                    ('Якість програмного забезпечення та тестування', 'ЯПЗтаТ')]

        if len(Subject.get_subjects()) > 0:
            return
        else:
            for subject in subjects:
                session.add(Subject(name=subject[1], fullname=subject[0]))

            session.commit()

        print('subjects added')

    @staticmethod
    def get_subjects():
        return session.query(Subject).all()

    @staticmethod
    def get_subject_fullname_by_id(subject_id):
        subject = session.query(Subject).get(subject_id)
        return subject.fullname

    @staticmethod
    def get_subject_name_by_id(subject_id):
        subject = session.query(Subject).get(subject_id)
        return subject.name


Base.metadata.create_all(conn)
