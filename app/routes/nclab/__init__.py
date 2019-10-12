from app import app
from flask import render_template
from sqlalchemy import desc
from app.routes.nclab import download, update, course

from app.models.nclab import *


@app.route('/nclab/', methods=["GET"])
def nclab():
    result_lec, result_attach, result_notice, result_hw = list(), list(), list(), list()

    for i in Lectures.query.all():
        result_lec.append(i.as_dict())

    for i in Attachments.query.order_by(Attachments.datetime.desc()).limit(10).all():
        temp_dict = i.as_dict()
        temp_dict['lec_name'] = i.lecture.name
        temp_dict['lec_semester'] = i.lecture.semester
        result_attach.append(temp_dict)

    for i in Documents.query.order_by(Documents.datetime.desc()).filter_by(board_type='d').limit(10).all():
        temp = i.as_dict()
        lec = Lectures.query.filter_by(id=temp['lecture_id']).first()
        temp['name'] = lec.name
        temp['semester'] = lec.semester
        result_notice.append(temp)

    for i in Documents.query.order_by(Documents.datetime.desc()).filter_by(board_type='rep').limit(10).all():
        temp = i.as_dict()
        lec = Lectures.query.filter_by(id=temp['lecture_id']).first()
        temp['name'] = lec.name
        temp['semester'] = lec.semester
        result_hw.append(temp)

    return render_template('nclab.html',
                           lectures=result_lec, attachments=result_attach, notice=result_notice, homeworks=result_hw)
