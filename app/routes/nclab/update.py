from flask import render_template, Blueprint,request
from app import app, Base

from sqlalchemy import exc
import requests

from app.tool.SNCP import lecture
from app.tool.SNCP import board
from app.tool.SNCP import document

from app.tool.Database.lecture_tool import document_checker

from app.models.nclab import Lectures
from app.models.nclab import Documents
from app.models.nclab import Attachments

index = Blueprint('update', __name__)


@index.route('/lec', methods=["GET"])
def update_lecture():
    nclab_lecture = lecture.lecture()

    for lec in nclab_lecture:
        arg = [lec['semester'], lec['name'], lec['Q & A'], lec['강의자료'], lec['공지사항'], lec['Report']]
        new_lecture = Lectures(*arg)

        lecture_check = Lectures.query.filter_by(semester=lec['semester'], name=lec['name']).all()

        if len(lecture_check) is 0:
            try:
                Base.session.add(new_lecture)
                Base.session.commit()
            except exc.SQLAlchemyError:
                return exc.SQLAlchemyError, 500

    return 'update complete', 200


@index.route('/board', methods=["GET"])
def update_board_content():
    request_lec = './lecture/' + request.args.get('lec') if request.args.get('lec') is not None else None

    if request_lec is None:
        return 'Please input Lecture Name'

    board_type = request_lec.split('_')[-1]

    if board_type == 'qna':
        check_board = Lectures.query.filter_by(qa=request_lec).all()
    elif board_type == 'n':
        check_board = Lectures.query.filter_by(lec=request_lec).all()
    elif board_type == 'd':
        check_board = Lectures.query.filter_by(notice=request_lec).all()
    elif board_type == 'rep':
        check_board = Lectures.query.filter_by(report=request_lec).all()
    else:
        return 'no type', 500

    if len(check_board) is not 1:
        return 'Invalid input', 500

    _document = board.Board(request.args.get('lec'))
    target_board = check_board[0]

    document_checker(_document, target_board.id, board_type)

    return 'update complete', 200


@index.route('/document', methods=["GET"])
def update_document():
    _documents = Documents.query.all()

    for doc in _documents:
        doc_content = document.Document(doc.link)

        try:
            doc_temp = Documents.query.filter_by(link=doc.link).first()
            doc_temp.content = doc_content.get_content()['content']
            Base.session.commit()
        except exc.SQLAlchemyError:
            return "Fail to add Document content", 500

    return "update complete", 200


@index.route('/attachment', methods=["GET"])
def update_attach():
    _documents = Documents.query.all()

    for doc in _documents:
        doc_content = document.Document(doc.link)

        for i in doc_content.get_attach():
            attachment_check = Attachments.query.filter_by(link=i['file_link']).all()

            if len(attachment_check) is 0:
                _doc = requests.session()
                _doc.get(doc.link)

                _file = _doc.get(i['file_link'])

                path = 'upload/' + i['file']

                with open(path, 'wb') as writer:
                    writer.write(_file.content)

                new_attach = Attachments(i['file'], i['date'], i['file_link'], doc.lecture_id, doc.id)

                try:
                    Base.session.add(new_attach)
                    Base.session.commit()
                except exc.SQLAlchemyError:
                    return "Update Failed : {0}".format(exc.SQLAlchemyError), 500

    return "update complete", 200


app.register_blueprint(index, url_prefix='/nclab/update')
