from flask import render_template
from app.routes import nclab, auth
from app import app


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/intro')
def intro():
    return render_template('introduce.html')
