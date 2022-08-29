from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = None

from app.routes import main, attendance, auth
app.register_blueprint(main.bp)
app.register_blueprint(attendance.bp)
app.register_blueprint(auth.bp)