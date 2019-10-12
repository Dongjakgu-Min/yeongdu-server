from flask import render_template, Blueprint,request
from app import app, Base

from sqlalchemy import exc
import requests

from app.tool.SNCP import lecture
from app.tool.SNCP import board
from app.tool.SNCP import document

from app.models.nclab import Lectures
from app.models.nclab import Documents
from app.models.nclab import Attachments


def document_checker(_document, _board_id, _type):
    for doc in _document.get_document():
        document_check = Documents.query.filter_by(link=doc['link']).all()

        if len(document_check) is 0:
            args = [doc['title'], doc['date'], doc['access'], doc['link'], _type, _board_id]
            new_doc = Documents(*args)

            try:
                Base.session.add(new_doc)
                Base.session.commit()
            except exc.SQLAlchemyError:
                return exc.SQLAlchemyError, 500


def find_lecture(lecture_name):
    board_type = lecture_name.split('_')[-1]
    lecture_name = './lecture/' + lecture_name

    if board_type == 'qna':
        check_board = Lectures.query.filter_by(qa=lecture_name).first()
    elif board_type == 'n':
        check_board = Lectures.query.filter_by(lec=lecture_name).first()
    elif board_type == 'd':
        check_board = Lectures.query.filter_by(notice=lecture_name).first()
    elif board_type == 'rep':
        check_board = Lectures.query.filter_by(report=lecture_name).first()
    else:
        return None

    if check_board is None:
        return None

    return check_board, board_type
