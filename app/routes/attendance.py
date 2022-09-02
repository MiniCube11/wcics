from threading import local
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session
from flask_login import current_user, login_required
from app import app, db
from app.forms import AttendanceForm, CreateAttendanceForm
from app.models import Attendance
from app.utils import format_time, is_valid_attendance, local_to_utc
import datetime

bp = Blueprint('attendance', __name__)

@bp.route('/here')
def attendance_redirect():
    return redirect(url_for('attendance.attendance'))

@bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    form = AttendanceForm()
    if form.validate_on_submit():
        code = form.code.data
    else:
        code = request.args.get('code')
    if code:
        attendance = Attendance.query.filter_by(code=code).first()
        if attendance and is_valid_attendance(attendance):
            if not attendance in current_user.attendance:
                attendance.attendees.append(current_user)
                db.session.commit()
            session['attendance_success'] = True
            return redirect(url_for('attendance.success'))
        flash("The code you entered is invalid.")
        return redirect(url_for('attendance.attendance'))
    return render_template('attendance/attendance.html', form=form)

@bp.route('/attendance/success')
def success():
    if not session.get('attendance_success'):
        return redirect(url_for('attendance.attendance'))
    session.pop('attendance_success', None)
    return render_template('attendance/success.html')

@bp.route('/attendance/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    form = CreateAttendanceForm()
    if request.method == 'GET':
        form.code.data = Attendance.random_code(length=6)
        form.date.data = datetime.datetime.now()
        form.start_time.data = datetime.datetime.now()
        form.end_time.data = datetime.datetime.now() + datetime.timedelta(hours=2)
    elif form.validate_on_submit():
        start_time = local_to_utc(datetime.datetime.combine(form.date.data, form.start_time.data))
        end_time = local_to_utc(datetime.datetime.combine(form.date.data, form.end_time.data))
        if end_time < start_time:
            end_time += datetime.timedelta(days=1)
        attendance = Attendance(code=form.code.data,
                                start_time=start_time,
                                end_time=end_time)
        if form.code.data == "" or Attendance.query.filter_by(code=form.code.data).first() is None:
            db.session.add(attendance)
            db.session.commit()
        else:
            flash("The attendance code has already been used.")
        return redirect(url_for('attendance.admin'))
    attendances = Attendance.query.order_by(Attendance.end_time.desc()).all()
    return render_template('attendance/admin.html', form=form, attendances=attendances, len=len, format_time=format_time, is_valid_attendance=is_valid_attendance)

@bp.route('/attendance/<code>/attendees')
@login_required
def attendees(code):
    if not current_user.is_admin:
        abort(403)
    attendance = Attendance.query.filter_by(code=code).first_or_404()
    return render_template('attendance/attendees.html', attendance=attendance)

@bp.route('/attendance/<code>/display')
@login_required
def display(code):
    if not current_user.is_admin:
        abort(403)
    attendance = Attendance.query.filter_by(code=code).first_or_404()
    return render_template('attendance/display.html', attendance=attendance)