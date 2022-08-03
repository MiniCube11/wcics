from flask import Flask

app = Flask(__name__)

from app.routes import main, attendance
app.register_blueprint(main.bp)
app.register_blueprint(attendance.bp)