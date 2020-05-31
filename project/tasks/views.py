from functools import wraps
from flask import flash, session, redirect, url_for, render_template, request, Blueprint
from project import db
from project.models import Task
from .forms import AddTaskForm
from datetime import datetime


tasks_blueprint = Blueprint('tasks', __name__)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Login First')
            return redirect(url_for('users.login'))

    return wrap


def flash_errors(form):
    for field, errors in form.error.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')


def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())


@tasks_blueprint.route('/tasks')
@login_required
def tasks():
    return render_template('tasks.html', form=AddTaskForm(request.form), open_tasks=open_tasks(), closed_tasks=closed_tasks(), username=session['username'], email=session['email'])


@tasks_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def new_task():
    error = None
    form = AddTaskForm(request.form)

    if request.method == 'POST':

        if form.validate_on_submit():
            task = Task(form.name.data, form.due_date.data, form.priority.data, '1', session['user_id'], datetime.utcnow())
            db.session.add(task)
            db.session.commit()
            flash('New Task Added!')
            return redirect(url_for('tasks.tasks'))
        else:
            return render_template('tasks.html', form=form, error=error)

    return render_template('tasks.html', error=error, form=form, open_tasks=open_tasks(), closed_tasks=closed_tasks())


@tasks_blueprint.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
    new_id = task_id

    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == 'admin':
        task.update({"status": 0})
        db.session.commit()
        flash('Task marked completed')
        return redirect(url_for('tasks.tasks'))
    else:
        flash('Only assigned user or admin can complete the task.')
        return redirect(url_for('tasks.tasks'))


@tasks_blueprint.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
    task = db.session.query(Task).filter_by(task_id=task_id)
    if session['user_id'] == task.first().user_id or session['role'] == 'admin':
        task.delete()
        db.session.commit()
        flash('Task Deleted')
        return redirect(url_for('tasks.tasks'))
    else:
        flash('Only assigned user or admin can delete the task.')
        return redirect(url_for('tasks.tasks'))
