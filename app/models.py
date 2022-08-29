from app import db, login
from flask_login import UserMixin

user_attendance = db.Table('user_attendance',
                            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                            db.Column('attendance_id', db.Integer, db.ForeignKey('attendance.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    attendance = db.relationship('Attendance', secondary=user_attendance, backref=db.backref('attendees', lazy='dynamic'))
    is_admin = db.Column(db.Boolean, index=True, default=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, index=True, unique=True)
    start_time = db.Column(db.DateTime, index=True)
    end_time = db.Column(db.DateTime, index=True)