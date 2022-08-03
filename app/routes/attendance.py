from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('attendance', __name__)


@bp.route('/here')
def attendance_redirect():
    return redirect(url_for('attendance.index'))

@bp.route('/attendance')
def index():
    return render_template('attendance/index.html')