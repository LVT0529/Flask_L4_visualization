from flask import Blueprint, render_template, url_for, jsonify, request, render_template_string, Flask, current_app
from werkzeug.utils import redirect

import subprocess
import threading

from pybo.static.visual_view import slb_ssh
from pybo.views.auth_views import login_required

from pybo import db
from pybo.models import afahvslb3_pool, afahvslb3_node

from sqlalchemy import update

bp = Blueprint('afahvslb3', __name__, url_prefix='/')

@bp.route('/afahvslb3', methods=('GET', 'POST'))
@login_required
def _afahvslb3():
    pool_data = afahvslb3_pool.query.all()
    node_data = afahvslb3_node.query.all()

    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    if kw:
        search = '%%{}%%'.format(kw)


    return render_template('slb_report/afahvslb3.html', pool_data = pool_data, node_data = node_data)

@bp.route('/afahvslb3/data', methods=('GET', 'POST'))
def _afahvslb3_data():
    return render_template('slb_report/SLB_data.html')


@bp.route('/afahvslb3/run_function', methods=['GET'])
def run_function():
    data_refresh('211.49.227.249', '211.49.227.250', '#ngkqns^ksAHV$lb')
    return 'Success'


def sorted_order(list):
    result = []

    for i in range(len(list)):
        temp = []
        count = 0

        for k in range(len(list)):

            if( (list[i][0] == list[k][0]) and (list[k] != [0])):
                list[k][3] = int(list[k][3])
                temp.append(list[k])

                if(count == 0):
                    count += 1
                else:
                    list[k] = [0]


        temp.sort(key=lambda x: x[3])

        if(len(temp) != 0):
            for j in range(len(temp)):
                result.append(temp[j])

    return result

def data_refresh(slb1, slb2, slb_pw):
    slb_pool, slb_node = slb_ssh(slb1, slb2, slb_pw)

    db.session.query(afahvslb3_pool).delete()
    db.session.query(afahvslb3_node).delete()
    db.session.commit()

    for i in range(len(slb_pool)):
        comment = afahvslb3_pool(id= i+1, pool = slb_pool[i][0], pool_status = slb_pool[i][2], pool_vip = slb_pool[i][1])
        db.session.add(comment)
        db.session.commit()

    for i in range(len(slb_node)):
        comment = afahvslb3_node(id= i+1, pool = slb_node[i][0], node = slb_node[i][1], node_port = slb_node[i][2], node_status = slb_node[i][4], pool_vip = slb_node[i][3])
        db.session.add(comment)
        db.session.commit()

