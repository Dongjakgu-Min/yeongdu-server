import asyncio

from app import app
from flask import render_template
from app.routes.nclab import download, update, course

from app.models.nclab import *


@app.route('/nclab/', methods=["GET"])
def nclab():
    result_lec, result_attach, result_notice, result_hw = list(), list(), list(), list()

    for i in Lectures.query.all():
        result_lec.append(i.as_dict())

    result_attach = attachment()
    result_notice = document()
    result_hw = homework()

    return render_template('nclab.html',
                           lectures=result_lec, attachments=result_attach,
                           notice=result_notice, homeworks=result_hw)


@app.route('/nclab/notice', methods=['GET'])
def nclab_notice():
    result_notice = list()

    for i in Documents.query.order_by(Documents.datetime.desc()).filter_by(board_type='d').limit(10).all():
        temp = i.as_dict()
        lec = Lectures.query.filter_by(id=temp['lecture_id']).first()
        temp['name'] = lec.name
        temp['semester'] = lec.semester
        result_notice.append(temp)

    return result_notice


@app.route('/nclab/homework', methods=['GET'])
def nclab_homework():
    result_hw = list()

    for i in Documents.query.order_by(Documents.datetime.desc()).filter_by(board_type='rep').limit(10).all():
        temp = i.as_dict()
        lec = Lectures.query.filter_by(id=temp['lecture_id']).first()
        temp['name'] = lec.name
        temp['semester'] = lec.semester
        result_hw.append(temp)

    return result_hw


def attachment():
    result_attach = list()

    for i in Attachments.query.order_by(Attachments.datetime.desc()).limit(10).all():
        temp_dict = i.as_dict()
        temp_dict['lec_name'] = i.lecture.name
        temp_dict['lec_semester'] = i.lecture.semester
        result_attach.append(temp_dict)

    return result_attach


def document():
    result_notice = list()

    for i in Documents.query.order_by(Documents.datetime.desc()).filter_by(board_type='d').limit(10).all():
        temp = i.as_dict()
        lec = Lectures.query.filter_by(id=temp['lecture_id']).first()
        temp['name'] = lec.name
        temp['semester'] = lec.semester
        result_notice.append(temp)

    return result_notice


def homework():
    result_hw = list()

    for i in Documents.query.order_by(Documents.datetime.desc()).filter_by(board_type='rep').limit(10).all():
        temp = i.as_dict()
        lec = Lectures.query.filter_by(id=temp['lecture_id']).first()
        temp['name'] = lec.name
        temp['semester'] = lec.semester
        result_hw.append(temp)

    return result_hw
