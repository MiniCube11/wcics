from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired

class AttendanceForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateAttendanceForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Create')