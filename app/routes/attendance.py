from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from app import app, db
from app.forms import AttendanceForm, CreateAttendanceForm
from app.models import Attendance
import datetime

bp = Blueprint('attendance', __name__)

@bp.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.is_admin:
        if current_user.email in app.config['ADMIN_USERS']:
            current_user.is_admin = True
            db.session.commit()

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
        current_time = datetime.datetime.utcnow()
        if attendance and attendance.start_time <= current_time <= attendance.end_time:
            attendance.attendees.append(current_user)
            db.session.commit()
            return redirect(url_for('attendance.success'))
        flash("The code you entered is invalid.")
        return redirect(url_for('attendance.attendance'))
    return render_template('attendance/attendance.html', form=form)

@bp.route('/attendance/success')
def success():
    return render_template('attendance/success.html')

@bp.route('/attendance/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    form = CreateAttendanceForm()
    if form.validate_on_submit():
        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        attendance = Attendance(code=form.code.data,
                                start_time=start_time,
                                end_time=end_time)
        db.session.add(attendance)
        db.session.commit()
        return redirect(url_for('attendance.admin'))
    attendances = Attendance.query.all()
    return render_template('attendance/admin.html', form=form, attendances=attendances)

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