from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.forms import AttendanceForm, CreateAttendanceForm
from app.models import Attendance
import datetime

bp = Blueprint('attendance', __name__)


@bp.route('/here')
def attendance_redirect():
    return redirect(url_for('attendance.index'))

@bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def index():
    form = AttendanceForm()
    if form.validate_on_submit():
        attendance = Attendance.query.filter_by(code=form.code.data).first()
        if attendance:
            attendance.attendees.append(current_user)
            db.session.commit()
            return redirect(url_for('attendance.attendance_success'))
        return redirect(url_for('attendance.index'))
    return render_template('attendance/index.html', form=form)

@bp.route('/attendance/success')
def attendance_success():
    return "The code you submitted was valid."

@bp.route('/attendance/admin',methods=['GET', 'POST'])
@login_required
def attendance_admin():
    form = CreateAttendanceForm()
    if form.validate_on_submit():
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        attendance = Attendance(code=form.code.data,
                                start_time=start_time,
                                end_time=end_time)
        db.session.add(attendance)
        db.session.commit()
        return redirect(url_for('attendance.attendance_admin'))
    attendances = current_user.attendance
    print(attendances)
    return render_template('attendance/admin.html', form=form, attendances=attendances)