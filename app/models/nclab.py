from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from app import Base
import re
import datetime


class Lectures(Base.Model):
    __table_name__ = 'nclab_lecture'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)

    semester = Base.Column(Base.String(30), nullable=False)
    name = Base.Column(Base.String(100), nullable=False)
    qa = Base.Column(Base.String(100), nullable=False)
    lec = Base.Column(Base.String(100), nullable=False)
    notice = Base.Column(Base.String(100), nullable=False)
    report = Base.Column(Base.String(100), nullable=False)

    def __init__(self, semester, name, qa, lec, notice, report):
        self.semester = re.sub(r'\(\)', '', semester)
        self.name = name
        self.qa = qa
        self.lec = lec
        self.notice = notice
        self.report = report

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Documents(Base.Model):
    __table_name__ = 'nclab_document'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)

    lecture_id = Base.Column(Base.Integer, ForeignKey('lectures.id'), nullable=False)
    lecture = relationship("Lectures", backref=backref('nclab_document', order_by=id))

    title = Base.Column(Base.String(100), nullable=False)
    datetime = Base.Column(Base.String(100), nullable=False)
    access = Base.Column(Base.Integer, nullable=False)
    link = Base.Column(Base.String(300), nullable=False)
    board_type = Base.Column(Base.String(5), nullable=False)
    content = Base.Column(Base.String(3000), nullable=True)

    def __init__(self, title, create_time, access, link, board_type, lecture_id):
        self.title = title
        self.access = access
        self.link = link
        self.board_type = board_type
        self.lecture_id = lecture_id

        try:
            self.datetime = datetime.datetime.strptime(create_time, '%m-%d')
        except ValueError:
            self.datetime = datetime.datetime.today()

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Attachments(Base.Model):
    __table_name__ = 'nclab_attachments'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)

    lecture_id = Base.Column(Base.Integer, ForeignKey('lectures.id'), nullable=False)
    document_id = Base.Column(Base.Integer, ForeignKey('documents.id'), nullable=False)

    document = relationship("Documents", backref=backref('nclab_documents', order_by=id))
    lecture = relationship("Lectures", backref=backref('nclab_comments', order_by=id))

    filename = Base.Column(Base.String(100), nullable=False)
    datetime = Base.Column(DateTime, nullable=False)

    link = Base.Column(Base.String(300), nullable=False)

    def __init__(self, filename, create_time, link, lecture_id, document_id):
        self.filename = filename
        self.datetime = datetime.datetime.strptime(create_time.split(': ')[-1], '%Y-%m-%d %H:%M:%S')
        self.link = link
        self.lecture_id = lecture_id
        self.document_id = document_id

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}


class Comments(Base.Model):
    __table_name__ = 'nclab_comment'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    id = Base.Column(Base.Integer, primary_key=True, autoincrement=True)

    lecture_id = Base.Column(Base.Integer, ForeignKey('lectures.id'), nullable=False)
    document_id = Base.Column(Base.Integer, ForeignKey('documents.id'), nullable=False)

    lecture = relationship("Lectures", backref=backref('nclab_attachment', order_by=id))
    document = relationship("Documents", backref=backref('nclab_attachment', order_by=id))

    content = Base.Column(Base.String(500), nullable=False)
    datetime = Base.Column(Base.String(100), nullable=False)

    def __init__(self, content, datetime, lecture_id, document_id):
        self.content = content
        self.datetime = datetime
        self.lecture_id = lecture_id
        self.document_id = document_id

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
