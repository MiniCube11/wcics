import datetime

def utc_to_local(utc_datetime):
    time_dif = datetime.datetime.now() - datetime.datetime.utcnow()
    return utc_datetime + time_dif

def local_to_utc(local_datetime):
    time_dif = datetime.datetime.now() - datetime.datetime.utcnow()
    return local_datetime - time_dif

def format_time(date):
    date = utc_to_local(date)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_date = datetime.datetime.now()
    
    day = f"{months[date.month-1]} {date.day}"
    if date.year == current_date.year and date.month == current_date.month and date.day == current_date.day:
        day = "Today"

    hour = date.hour
    suffix = "am"
    if hour >= 12:
        hour -= 12
        suffix = "pm"
    if hour == 0:
        hour = 12
    
    minute = str(date.minute)
    if len(minute) == 1:
        minute = "0" + minute
    
    return f"{day} {hour}:{minute}{suffix}"

def is_valid_attendance(attendance):
    current_time = datetime.datetime.utcnow()
    return attendance.start_time <= current_time <= attendance.end_time