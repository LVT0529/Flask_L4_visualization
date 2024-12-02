from flask import Blueprint, render_template, url_for, jsonify, request, render_template_string, Flask, current_app
from werkzeug.utils import redirect

import subprocess
import threading
import requests
import time

from pybo.static.visual_view import slb_ssh
from pybo.views.auth_views import login_required

from pybo import db
from pybo.models import afmainslb_pool, afmainslb_node

from sqlalchemy import update

bp = Blueprint('integrated', __name__, url_prefix='/')

@bp.route('/integrated', methods=('GET', 'POST'))
@login_required
def _integrated():
    pool_data = afmainslb_pool.query.all()
    node_data = afmainslb_node.query.all()

    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')

    if kw:
        search = '%%{}%%'.format(kw)

        '''
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문 제목
                    Question.content.ilike(search) |  # 질문 내용
                    User.username.ilike(search) |  # 질문 작성자
                    sub_query.c.content.ilike(search) |  # 답변 내용
                    sub_query.c.username.ilike(search)  # 답변 작성자
                    ) \
            .distinct()
        '''

    return render_template('slb_report/integrated_data.html', pool_data = pool_data, node_data = node_data)

@bp.route('/integrated/data', methods=('GET', 'POST'))
def _afmainslb_data():
    return render_template('slb_report/SLB_data.html')


@bp.route('/integrated/run_function', methods=['GET'])
def run_function():
    data_refresh('118.218.124.251', '118.218.124.252', '#ngkqns^ks5fm$lb')
    return 'Success'


@bp.route('/slb_data/run_function', methods=['GET'])
def slb_data():
    response = requests.get('http://114.200.198.229:5000/afmainslb/run_function')
    print(response.status_code)
    #requests.get('http://114.200.198.229:5000/afreecaslb/run_function')
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

    db.session.query(afmainslb_pool).delete()
    db.session.query(afmainslb_node).delete()
    db.session.commit()

    for i in range(len(slb_pool)):
        comment = afmainslb_pool(id= i+1, pool = slb_pool[i][0], pool_status = slb_pool[i][2], pool_vip = slb_pool[i][1])
        db.session.add(comment)
        db.session.commit()

    for i in range(len(slb_node)):
        comment = afmainslb_node(id= i+1, pool = slb_node[i][0], node = slb_node[i][1], node_port = slb_node[i][2], node_status = slb_node[i][4], pool_vip = slb_node[i][3])
        db.session.add(comment)
        db.session.commit()

