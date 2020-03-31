from database.database import *


class GradeType(Base):
    __tablename__ = 'gradetype'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(256))

    @staticmethod
    def add_gradetypes():
        if len(session.query(GradeType).all()) > 0:
            return
        else:
            grade_types = ['Модульний контроль 1', 'Модульний контроль 2', 'Залік', 'Диференційний залік', 'Екзамен']

            for grade_type in grade_types:
                session.add(GradeType(name=grade_type))
                session.commit()

            print("grade_types added")

    @staticmethod
    def get_gradetype_by_id(gradetype_id):
        gradetype = session.query(GradeType).get(gradetype_id)
        return gradetype.name

    @staticmethod
    def get_gradetypes():
        return [gradetype for gradetype in session.query(GradeType).all()]


Base.metadata.create_all(conn)
