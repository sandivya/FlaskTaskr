from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('__config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.tasks.views import tasks_blueprint
from project.users.views import users_blueprint
from project.api.views import api_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)


@app.errorhandler(404)
def not_found(error):
    if app.debug is not True:
        now = datetime.now()
        r = request.url
        with open('error.log', 'a') as log_file:
            current_time = now.strftime("%d-%m-%Y %H:%M:%S")
            log_file.write("\n404 error at {} : {}".format(current_time, r))
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    if app.debug is not True:
        now = datetime.now()
        r = request.url
        with open('error.log', 'a') as log_file:
            current_time = now.strftime("%d-%m-%Y %H:%M:%S")
            log_file.write("\n500 error at {} : {}".format(current_time, r))
    return render_template('500.html'), 500
