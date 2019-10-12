from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from app import Base


class User(Base.Model):
    __table_name__ = 'users'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)
    level = Base.Column(Base.Integer, nullable=False)
    user_id = Base.Column(Base.String(10), nullable=False)
    user_pw = Base.Column(Base.String(10), nullable=False)
    email = Base.Column(Base.String(20), nullable=False)

    def __init__(self, user_id, user_pw, email):
        self.user_id = user_id
        self.user_pw = user_pw
        self.email = email
