from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect


from pybo.models import Question



bp = Blueprint('visual', __name__, url_prefix='/')

@bp.route('/visual', methods=('GET', 'POST'))
def _visual():
    return render_template('visual/L4_visual.html')
