from flask import Blueprint, render_template
from app.constants import faq

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html', faq=faq, home=True)
