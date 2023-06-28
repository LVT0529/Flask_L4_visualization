from flask import Blueprint, render_template, url_for, jsonify, request, render_template_string, Flask, send_file
from werkzeug.utils import redirect

import requests
import subprocess
import datetime
import time

import pandas as pd
import io
import os

from pybo.views.auth_views import login_required
from pybo.static.network_script import network_report



from pybo import db
from pybo.models import L4_wideip, L4_pool, L4_pool_option, L4_poolmbr, L4_poolmbr_option

from sqlalchemy import update




#app = Flask(__name__, static_folder="static", static_url_path="/static")
bp = Blueprint('network', __name__, url_prefix='/')
#bp = Blueprint('visual', __name__, static_folder="static", static_url_path="/static")


@bp.route('/network', methods=('GET', 'POST'))
@login_required
def _network():
    return render_template('visual/network_report.html')



@bp.route('/network/result', methods=('GET', 'POST'))
def _network_result():

    if request.method == 'POST':
        ad_id = request.form.get('ad_id')
        ad_pw = request.form.get('ad_pw')
        input_value1 = request.form.get('input_field1')
        input_value2 = request.form.get('input_field2')
        input_value3 = request.form.get('input_field3')
        input_value4 = request.form.get('input_field4')
        input_file = request.files.getlist('file_field1')

        network_report(ad_id, ad_pw, input_value1, input_value2, input_value3, input_value4, input_file)

        return render_template('visual/network_result.html')
        #return send_file(file_path, as_attachment=True)


        # 입력 값 처리 로직을 여기에 작성


@bp.route('/network/download_file', methods=('GET', 'POST'))
def download_file():
    nowdate = datetime.datetime.now()
    report_file = nowdate.strftime("%Y-%m-%d") + ' Montly Report.xlsx'

    file_path = os.getcwd() + '\\' + report_file


    return send_file(file_path, as_attachment=True)
