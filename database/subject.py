from database.database import *


class Subject(Base):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256))

    @staticmethod
    def add_subjects():
        subjects = ['ООП', 'ОПИ', 'АВдоПЗ', 'ГДіК', 'ЯПЗтаТ']

        if len(Subject.get_subjects()) > 0:
            return
        else:
            for subject in subjects:
                session.add(Subject(name=subject))

            session.commit()

        print('subjects added')

    @staticmethod
    def get_subjects():
        return session.query(Subject).all()

    @staticmethod
    def get_subject_by_id(subject_id):
        subject = session.query(Subject).get(subject_id)
        return subject.name


Base.metadata.create_all(conn)
