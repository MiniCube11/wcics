from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired

class AttendanceForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Submit')
