from functools import wraps
from flask import flash, request, redirect, render_template, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from .forms import LoginUser, AddUserForm
from project.models import User
from project import db, bcrypt

# Config
users_blueprint = Blueprint('users', __name__)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Login First')
            return redirect(url_for('users.login'))

    return wrap


@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Goodbye!')
    return redirect(url_for('users.login'))


@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    form = LoginUser(request.form)
    error = None
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user is not None and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.name.split()[0]
            session['email'] = user.email
            flash('Login Successful!')
            return redirect(url_for('tasks.tasks'))
        else:
            error = 'Invalid Credentials'

    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = AddUserForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.name.data, bcrypt.generate_password_hash(form.password.data).decode('utf-8'), form.email.data)
            # new_user = User(form.name.data, form.password.data, form.email.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registered Successfully. Login Now')
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'Email already exists.'
                return render_template('register.html', form=form, error=error)
        else:
            flash('Invalid Form Data')

    return render_template('register.html', form=form)
