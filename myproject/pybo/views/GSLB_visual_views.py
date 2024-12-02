from flask import Blueprint, render_template, url_for, jsonify, request, render_template_string, Flask, current_app
from werkzeug.utils import redirect

import subprocess
import threading

from pybo.static.visual_view import wideip, pool, wideip_ssh, widepool_ssh, pool_ssh, poolpoolmbr_ssh, poolmbr_ssh
from pybo.views.auth_views import login_required

from pybo import db
from pybo.models import L4_wideip, L4_pool, L4_pool_option, L4_poolmbr, L4_poolmbr_option

from sqlalchemy import update

bp = Blueprint('visual', __name__, url_prefix='/visual')

@bp.route('/visual', methods=('GET', 'POST'))
@login_required
def _visual():
    wideip_data = L4_wideip.query.all()
    wp_mapp_data = L4_pool.query.all()
    pool_data = L4_pool_option.query.all()
    ppmbr_mapp_data = L4_poolmbr.query.all()


    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    
    wideip_list = L4_wideip.query.order_by(L4_wideip.id.asc())

    per_page = request.args.get('per_page', 20, type=int)


    if kw:
        search = '%%{}%%'.format(kw)

        wideip_list = wideip_list \
            .outerjoin(L4_pool, L4_wideip.wideip == L4_pool.wideip) \
            .outerjoin(L4_poolmbr, L4_pool.pool == L4_poolmbr.pool) \
            .filter(L4_wideip.wideip.ilike(search) |
                    L4_pool.pool.ilike(search) |
                    L4_poolmbr.poolmbr.ilike(search) |
                    L4_poolmbr.poolmbr_ip.ilike(search) |
                    L4_wideip.wideip_lbmod.ilike(search)
                    ) \
            .distinct()
        wideip_list = wideip_list.paginate(page=page, per_page=999)
    else:
        wideip_list = wideip_list.paginate(page=page, per_page=per_page)

    return render_template('visual/L4_visual.html', wideip_data = wideip_data, wp_mapp_data = wp_mapp_data, pool_data = pool_data, ppmbr_mapp_data = ppmbr_mapp_data, wideip_list = wideip_list, page=page, kw=kw, per_page=per_page)

@bp.route('/visual/data', methods=('GET', 'POST'))
def _visual_data():
    return render_template('visual/L4_data.html')


@bp.route('/visual/wideip', methods=('GET', 'POST'))
def _wideip_options():
    wideip_data = L4_wideip.query.all()
    wp_mapp_data = L4_pool.query.all()
    pool_data = L4_pool_option.query.all()
    ppmbr_mapp_data = L4_poolmbr.query.all()
    return render_template('visual/L4_wideip_options.html', wideip_data = wideip_data, wp_mapp_data = wp_mapp_data, pool_data = pool_data, ppmbr_mapp_data = ppmbr_mapp_data)

@bp.route('/visual/pool', methods=('GET', 'POST'))
def _pool_options():
    wideip_data = L4_wideip.query.all()
    wp_mapp_data = L4_pool.query.all()
    pool_data = L4_pool_option.query.all()
    ppmbr_mapp_data = L4_poolmbr.query.all()
    return render_template('visual/L4_pool_options.html', wideip_data = wideip_data, wp_mapp_data = wp_mapp_data, pool_data = pool_data, ppmbr_mapp_data = ppmbr_mapp_data)





@bp.route('/visual/run_function', methods=['GET'])
def run_function():
    data_refresh()
    return "Function executed successfully!"    

def sorted_order(list, num):
    result = []
    num = int(num)

    for i in range(len(list)):
        temp = []
        count = 0

        for k in range(len(list)):

            if( (list[i][0] == list[k][0]) and (list[k] != [0])):
                list[k][3 + num] = int(list[k][3 + num])
                temp.append(list[k])

                if(count == 0):
                    count += 1
                else:
                    list[k] = [0]


        temp.sort(key=lambda x: x[3 + num])

        if(len(temp) != 0):
            for j in range(len(temp)):
                result.append(temp[j])

    return result

def data_refresh():


        wideip = wideip_ssh()
        db.session.query(L4_wideip).delete()
        db.session.commit()

        for i in range(len(wideip)):
            wideip_data = L4_wideip.query.filter_by(wideip = wideip[i][0]).first()
            if(wideip_data):
                wideip_data.id = i + 1
                wideip_data.wideip_record = wideip[i][1]
                wideip_data.wideip_status = wideip[i][2]
                wideip_data.wideip_en = wideip[i][3]
                wideip_data.wideip_lbmod = wideip[i][4]
                wideip_data.wideip_rcof = wideip[i][5]
            else:
                comment = L4_wideip(id= i+1, wideip = wideip[i][0], wideip_record = wideip[i][1], wideip_status = wideip[i][2],
                                    wideip_en = wideip[i][3], wideip_lbmod = wideip[i][4], wideip_rcof = wideip[i][5])
                db.session.add(comment)
            db.session.commit()

        wp_mapp = widepool_ssh()
        wp_mapp = sorted_order(wp_mapp, 0)
        db.session.query(L4_pool).delete()
        db.session.commit()

        for i in range(len(wp_mapp)):
            pool = L4_pool.query.filter_by(pool = wp_mapp[i][1]).first()
            id = L4_pool.query.filter_by(id = i + 1).first()

            if(pool and id):
                L4_pool.wideip = wp_mapp[i][0]
                L4_pool.ratio = wp_mapp[i][2]
                L4_pool.order = wp_mapp[i][3]
            else:
                comment = L4_pool(id= i+1, wideip = wp_mapp[i][0], pool = wp_mapp[i][1], ratio = wp_mapp[i][2], order = wp_mapp[i][3])
                db.session.add(comment)

            db.session.commit()


        pool = pool_ssh()
        db.session.query(L4_pool_option).delete()
        db.session.commit()

        for i in range(len(pool)):

            comment = L4_pool_option(id= i+1, pool = pool[i][0], pool_ttl = pool[i][1], pool_status = pool[i][2], pool_en = pool[i][3],
                                         pool_lbmod = pool[i][4], pool_alter = pool[i][5], pool_fallback = pool[i][6], pool_avail = pool[i][7])
            db.session.add(comment)

            db.session.commit()



        ppmbr_mapp = poolpoolmbr_ssh()
        ppmbr_mapp = sorted_order(ppmbr_mapp, 1)
        db.session.query(L4_poolmbr).delete()
        db.session.commit()

        for i in range(len(ppmbr_mapp)):
            poolmbr = L4_poolmbr.query.filter_by(poolmbr = ppmbr_mapp[i][1]).first()
            id = L4_poolmbr.query.filter_by(id = i + 1).first()

            if(id and poolmbr):
                poolmbr.pool = ppmbr_mapp[i][0]
                poolmbr.ratio = ppmbr_mapp[i][2]
                poolmbr.order = ppmbr_mapp[i][3]
                poolmbr.poolmbr_status = ppmbr_mapp[i][4]
            else:
                comment = L4_poolmbr(id= i+1, pool = ppmbr_mapp[i][0], poolmbr = ppmbr_mapp[i][1], poolmbr_ip = ppmbr_mapp[i][2], ratio = ppmbr_mapp[i][3], order = ppmbr_mapp[i][4], poolmbr_status = ppmbr_mapp[i][5])
                db.session.add(comment)

            db.session.commit()
