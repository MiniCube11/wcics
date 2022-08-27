from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

class AttendanceForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateAttendanceForm(FlaskForm):
    code = StringField('Code')
    # start_time = DateField('Start Time', validators=[DataRequired()])
    # end_time = DateField('End Time', validators=[DataRequired()], format='%d.%m.%Y %H.%M')
    submit = SubmitField('Create')