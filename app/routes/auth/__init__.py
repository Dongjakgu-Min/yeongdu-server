from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, Base
from app.models.users import Users

from app.routes.auth import mypage


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        check = Users.query.filter_by(username=username).first()

        if check_password_hash(check.password, password) is True:
            session['login'] = True
            session['username'] = username
            return redirect('/')
        else:
            return redirect('/login')


@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hash_pw = generate_password_hash(password)

        check = Users.query.filter_by(username=username,
                                      email=email).first()
        if check is None:
            Base.session.add(Users(username, hash_pw, email))
            Base.session.commit()
            return redirect('/login')
        else:
            return "login ERRor"
