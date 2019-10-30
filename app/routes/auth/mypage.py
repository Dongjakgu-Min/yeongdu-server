from flask import Flask, render_template, request, redirect, session, url_for

from app import app, Base
from app.models.users import Users
from app.models.mail import Mails
from app.models.nclab import Lectures
from app.tool.Database import lecture_tool


@app.route('/mypage')
def mypage():
    if session.get('login') is None:
        return redirect('/login')

    temp = Users.query.filter_by(username=session.get('username')).first()

    mail_set = Mails.query.filter_by(user_id=temp.id).all()
    ca_set, cn_set = False, False

    ca_lec = Lectures.query.filter_by(code='class_201902_k1').first()
    cn_lec = Lectures.query.filter_by(code='class_201902_k2').first()

    for mail in mail_set:
        if mail.lecture_id == cn_lec.id:
            cn_set = True
        if mail.lecture_id == ca_lec.id:
            ca_set = True

    return render_template('auth/mypage.html', ca=ca_set, cn=cn_set)


@app.route('/mypage/emailService', methods=["POST"])
def mail_sender():
    if request.form.get('setEmail') is None:
        usr = Users.query.filter_by(username=session.get('username')).first()
        email = usr.email
    else:
        email = request.form.get('addr-email')

    item = Mails.query.filter_by(email=email).all()
    ca_set, cn_set = False, False

    ca_lec = Lectures.query.filter_by(code='class_201902_k1').first()
    cn_lec = Lectures.query.filter_by(code='class_201902_k2').first()

    for i in item:
        if ca_lec.id == i.lecture_id:
            ca_set = True
        if cn_lec.id == i.lecture_id:
            cn_set = True

    print('property : {0}'.format(request.form.get('ca-email')))

    if request.form.get('ca-email') is not None and ca_set is False:
        newbie = Mails(email, '201902_k1', usr.id, ca_lec.id)
        Base.session.add(newbie)
        Base.session.commit()
    elif request.form.get('ca-email') is None and ca_set is True:
        obj = Mails.query.filter_by(user_id=usr.id, lecture_id=1).first()
        Base.session.delete(obj) if obj is not None else None
        Base.session.commit()

        print('type : {0}'.format(type(cn_set)))

    if request.form.get('cn-email') is not None and cn_set is False:
        newbie = Mails(email, '201902_k2', usr.id, cn_lec.id)
        Base.session.add(newbie)
        Base.session.commit()
    elif request.form.get('cn-email') is None and cn_set is True:
        obj = Mails.query.filter_by(user_id=usr.id, lecture_id=2).first()
        Base.session.delete(obj) if obj is not None else None
        Base.session.commit()

    return redirect('/mypage')
