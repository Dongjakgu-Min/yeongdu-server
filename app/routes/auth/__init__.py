from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, Base
from app.models.users import Users

from app.routes.auth import mypage
from app.routes.form import LoginForm, SignupForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()

        return render_template('auth/login.html', form=form)
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pw']

        check = Users.query.filter_by(username=username).first()
        if check is None:
            return redirect('/signup')

        if check_password_hash(check.password, password) is True:
            session['login'] = True
            session['username'] = username
            return redirect('/')
        else:
            return redirect('/login')


@app.route('/logout', methods=['POST'])
def logout():
    session['login'] = None
    session['username'] = None
    return redirect('/')


@app.route('/signup',  methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        form = SignupForm()

        return render_template("auth/signup.html", form=form)
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pw']
        email = request.form['email']

        if len(username) < 6 or len(password) < 6:
            return redirect('/signup')

        hash_pw = generate_password_hash(password)

        check = Users.query.filter_by(username=username,
                                      email=email).first()
        if check is None:
            Base.session.add(Users(username, hash_pw, email))
            Base.session.commit()
            return redirect('/login')
        else:
            return "login ERRor"
