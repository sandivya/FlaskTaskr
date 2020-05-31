from project import db
import datetime


class Task(db.Model):

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted_date = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())

    def __init__(self, name, due_date, priority, status, user_id, posted_date):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.user_id = user_id
        self.posted_date = posted_date

    def __repr__(self):
        return '<name {0}>'.format(self.name)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False, default='user')
    tasks = db.relationship('Task', backref='poster')

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User {0}>'.format(self.name)
