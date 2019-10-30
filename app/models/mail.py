from sqlalchemy.orm import relationship, backref

from app import Base


class Mails(Base.Model):
    __table_name__ = 'mails'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    email = Base.Column(Base.String(20), nullable=False)
    lecture_id = Base.Column(Base.Integer, nullable=False)
    user_id = Base.Column(Base.Integer, nullable=False)

    def __init__(self, email, lecture_code, user_id, board_id):
        self.email = email
        self.lecture_code = lecture_code
        self.user_id = user_id
        self.lecture_id = board_id

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
