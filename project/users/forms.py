from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, Email


class AddUserForm(FlaskForm):
    id = IntegerField()
    name = StringField('Name', validators=[DataRequired(), Length(min=6, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    confirm = PasswordField('Repeat', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=50)])


class LoginUser(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
