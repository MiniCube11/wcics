import datetime

def is_valid_attendance(attendance):
    current_time = datetime.datetime.utcnow()
    return attendance.start_time <= current_time <= attendance.end_time