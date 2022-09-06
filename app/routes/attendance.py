from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, session
from flask_login import current_user, login_required
from app import db
from app.forms import AttendanceForm
from app.models import Attendance
from app.utils import is_valid_attendance
import json

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
    attendances = Attendance.query.order_by(Attendance.end_time.desc()).all()
    return render_template('attendance/admin.html', attendances=attendances, len=len, is_valid_attendance=is_valid_attendance)

@bp.route('/attendance/create', methods=['POST'])
@login_required
def create_attendance():
    if not current_user.is_admin:
        abort(403)
    res = request.get_data("data")
    data = json.loads(res)
    code = data.get("code")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    
    if not (start_time and end_time):
        return "Missing or empty fields."
    if not code:
        code = Attendance.random_code(length=6)

    attendance = Attendance(code=code, start_time=start_time, end_time=end_time)
    if Attendance.query.filter_by(code=code).first() is None:
        db.session.add(attendance)
        db.session.commit()
        return "Attendance code created successfully."
    return "Attendance code already exists."

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