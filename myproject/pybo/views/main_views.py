from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect


from pybo.models import Question
from pybo.views.auth_views import login_required


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@bp.route('/question')
def list():
    return redirect(url_for('question._list'))


@bp.route('/visual')
def l4visual():
    return redirect(url_for('visual._visual'))





@bp.route('/hello')
def hello_pybo():
    return 'Hello, pybo!'
