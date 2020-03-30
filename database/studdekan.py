from database.database import *


class Studdekan(Base):
    __tablename__ = 'studdekan'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True)
    student_id = sa.Column(sa.Integer, sa.ForeignKey('student.id'))

    student = relationship('Student')


Base.metadata.create_all(conn)
