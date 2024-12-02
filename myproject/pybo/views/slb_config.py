from flask import Blueprint, render_template, url_for, jsonify, request, render_template_string, Flask, current_app, send_file, abort
from werkzeug.utils import redirect

import os
import requests
import subprocess
import threading
import datetime

from pybo.views.auth_views import login_required

from pybo.static.slb_script import sconfig_report


bp = Blueprint('sconfig', __name__, url_prefix='/sconfig')

@bp.route('/sconfig', methods=('GET', 'POST'))
@login_required
def _sconfig():
    return render_template('slb_config/SLB_config.html')

@bp.route('/download/slb_config', methods=('GET', 'POST'))
def download_file():
    FILE_DIRECTORY = os.getcwd() + '/pybo/templates/slb_config/slb_config template.xlsx'
    try:
        return send_file(FILE_DIRECTORY, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found!")
        #abort(404, description=FILE_DIRECTORY)


@bp.route('/sconfig/result', methods=('GET', 'POST'))
def _sconfig_result():
    if request.method == 'POST':
        input_file = request.files['sconfig_file']
        sconfig_report(input_file)

        return render_template('slb_config/SLB_config_result.html')

@bp.route('/download/result_config', methods=('GET', 'POST'))
def download_result_file():

    nowdate = datetime.datetime.now()
    filename = nowdate.strftime("%m-%d") + ' CLI config Report.xlsx'
    FILE_DIRECTORY = os.getcwd() + '/' + filename

    try:
        return send_file(FILE_DIRECTORY, as_attachment=True)
    except FileNotFoundError:
        abort(404, description="File not found!")
        #abort(404, description=FILE_DIRECTORY)

