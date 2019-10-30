from app import app, Base

from sqlalchemy import exc

from app.models.nclab import Lectures
from app.models.nclab import Documents
from app.models.mail import Mails

from app.tool.Mailer.send import send_mail


def document_checker(_document, _board_id, _type):
    for doc in _document.get_document():
        document_check = Documents.query.filter_by(link=doc['link']).all()

        if len(document_check) is 0:
            args = [doc['title'], doc['date'], doc['access'], doc['link'], _type, _board_id]
            new_doc = Documents(*args)

            try:
                Base.session.add(new_doc)
                Base.session.commit()

                sub = Mails.query.filter_by(lecture_id=_board_id).all()
                for p in sub:
                    send_mail(p.email, _board_id, doc['title'])

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
