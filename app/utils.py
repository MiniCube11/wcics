import datetime

def utc_to_local(utc_datetime):
    time_dif = datetime.datetime.now() - datetime.datetime.utcnow()
    return utc_datetime + time_dif

def format_time(date):
    date = utc_to_local(date)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_date = datetime.datetime.utcnow()
    if date.year == current_date.year and date.month == current_date.month and date.day == current_date.day:
        formatted = "Today"
    else:
        formatted = f"{months[date.month-1]} {date.day}"
    if date.hour == 0:
        formatted += f"12:{date.minute}am"
    elif date.hour > 12:
        formatted += f" {date.hour-12}:{date.minute}pm"
    else:
        formatted += f" {date.hour}:{date.minute}am"
    return formatted

def is_valid_attendance(attendance):
    current_time = datetime.datetime.utcnow()
    return attendance.start_time <= current_time <= attendance.end_time