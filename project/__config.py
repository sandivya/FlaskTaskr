import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "flasktaskr.db"
SECRET_KEY = "my_secret_key"
WTF_CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

DEBUG = False
