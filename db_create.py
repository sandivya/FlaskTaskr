from project import db, bcrypt
import sqlite3
from project.__config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    cur = connection.cursor()

    # DB Operations cleared for safety reasons
