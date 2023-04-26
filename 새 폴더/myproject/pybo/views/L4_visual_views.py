from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
import requests

from pybo.models import Question



bp = Blueprint('visual', __name__, url_prefix='/')

@bp.route('/visual', methods=('GET', 'POST'))
def _visual():
    #response = requests.get(url = 'http://211.49.171.10/mgmt/tm/gtm/pool/a/pool_bjapi.afgslb.afreecatv.com/members')
    '''
    url_test = 'http://211.49.171.10/mgmt/tm/gtm/pool/a/pool_bjapi.afgslb.afreecatv.com/members'
    username = 'afguest'
    password = 'dk#mSLBguest'


    response = requests.get(url = url_test, verify = False, timeout=10, auth=(username, password) )

    return render_template('visual/L4_visual.html', data=response.text)
    '''
    return render_template('visual/L4_visual.html')
