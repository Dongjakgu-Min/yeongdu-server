import asyncio

from app import app
from flask import render_template
from app.routes.nclab import download, update, course

from app.models.nclab import *


@app.route('/nclab/', methods=["GET"])
def nclab():
    result_lec, result_attach, result_notice, result_hw = list(), list(), list(), list()

    lecture = Lectures.query.all()
    result_lec = [x.as_dict() for x in lecture]

    print(result_lec)

    result_attach = attachment()
    result_notice = document()
    result_hw = homework()

    return render_template('nclab.html',
                           lectures=result_lec, attachments=result_attach,
                           notice=result_notice, homeworks=result_hw)

@app.route('/nclab/notice', methods=['GET'])
def nclab_notice():
    notices = Documents.query.order_by(Documents.datetime.desc()) \
        .filter_by(board_type='d').limit(10).all()
    return [x.as_dict() for x in notices]


@app.route('/nclab/homework', methods=['GET'])
def nclab_homework():
    documents = Documents.query.order_by(Documents.datetime.desc()) \
        .filter_by(board_type='rep').limit(10).all()
    return [x.as_dict() for x in documents]


def attachment():
    attachments = Attachments.query.order_by(Attachments.datetime.desc()) \
        .limit(10).all()
    return [x.as_dict() for x in attachments]


def document():
    documents = Documents.query.order_by(Documents.datetime.desc()) \
        .filter_by(board_type='d').limit(10).all()
    return [x.as_dict() for x in documents]


def homework():
    homeworks = Documents.query.order_by(Documents.datetime.desc()) \
        .filter_by(board_type='rep').limit(10).all()
    return [x.as_dict() for x in homeworks]
