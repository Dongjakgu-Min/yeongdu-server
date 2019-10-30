from flask import Blueprint, render_template

from app import app, Base
from app.models.nclab import Lectures, Documents, Attachments
from app.tool.SNCP import lecture, document, board
from app.tool.Database import lecture_tool

index = Blueprint('/lecture', __name__)


@index.route('/<lecture_name>', methods=["GET"])
def lecture_nclab(lecture_name):
    if lecture_name is None:
        return 404

    result = list()

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
        return 'no type', 500

    for doc in Documents.query.filter_by(lecture_id=check_board.id, board_type=board_type):
        temp = doc.as_dict()
        attach_list = list()

        attachments = Attachments.query.filter_by(document_id=doc.id).all()
        for attach in attachments:
            attach_list.append(attach.as_dict())
        temp['attach'] = attach_list

        result.append(temp)

    return render_template('nclab_lecture.html', documents=result, lec=check_board.name)


@index.route('/<lecture_name>/update', methods=["POST"])
def lecture_update(lecture_name):
    target_lec, _type = lecture_tool.find_lecture(lecture_name)
    _board = board.Board(lecture_name)

    lecture_tool.document_checker(_board, target_lec.id, _type)

    return 'update complete', 200


app.register_blueprint(index, url_prefix='/nclab/lecture')
