from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):

    task_id = IntegerField()
    name = StringField('Task Name:', validators=[DataRequired()])
    due_date = DateField('Date Due (DD-MM-YYYY):', validators=[DataRequired()])
    priority = SelectField('Priority: ', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    status = IntegerField('Status')
