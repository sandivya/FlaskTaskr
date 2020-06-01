from functools import wraps
from flask import Blueprint, session, redirect, url_for, flash, jsonify, make_response
from project.models import Task
from project import db

api_blueprint = Blueprint('api', __name__)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Login First')
            return redirect(url_for('users.login'))

    return wrap


def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())


@api_blueprint.route('/api/v1/tasks/')
def api_tasks():

    results = db.session.query(Task).limit(10).offset(0).all()
    json_results = []

    for result in results:
        data = {
            'task_id': result.task_id,
            'task_name': result.name,
            'due_date': str(result.due_date),
            'priority': result.priority,
            'status': result.status,
            'posted_date': str(result.posted_date),
            'user_id': result.user_id
        }
        json_results.append(data)

    return jsonify(items=json_results)


@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id):

    fetched_task = db.session.query(Task).filter_by(task_id=task_id).first()

    if fetched_task:
        json_result = {
            'task_id': fetched_task.task_id,
            'task_name': fetched_task.name,
            'due_date': str(fetched_task.due_date),
            'priority': fetched_task.priority,
            'status': fetched_task.status,
            'posted_date': str(fetched_task.posted_date),
            'user_id': fetched_task.user_id
        }
        status_code = 200
    else:
        json_result = {"Error": 'Task does not exists'}
        status_code = 404

    # return make_response(jsonify(items=json_result), status_code)
    return make_response(jsonify(items=json_result), 404)
