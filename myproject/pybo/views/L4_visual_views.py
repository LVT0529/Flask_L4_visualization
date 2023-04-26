from flask import Blueprint, render_template, url_for, jsonify, request, render_template_string, Flask
from werkzeug.utils import redirect

import requests
import subprocess

from pybo.static.visual_view import wideip, pool, wideip_ssh

from pybo import db
from pybo.models import L4_wideip




#app = Flask(__name__, static_folder="static", static_url_path="/static")
bp = Blueprint('visual', __name__, url_prefix='/')
#bp = Blueprint('visual', __name__, static_folder="static", static_url_path="/static")





tree_data = [
    {
        'id': 1,
        'name': 'Node 123123',
        'label' : 'Parent Node',
        'scopedSlotsData': {
            "mySlotProperty": "Value for my slot property"
         },
        'children': [
            {
                'id': 2,
                'name': 'Child Node 1'
            },
            {
                'id': 3,
                'name': 'Child Node 2'
            }
        ]
    },
    {
        'id': 4,
        'name': 'Node 2'
    },
    {
        'id': 5,
        'name': 'Node 3',
        'children': [
            {
                'id': 6,
                'name': 'Child Node 3'
            }
        ]
    }
]

@bp.route('/visual', methods=('GET', 'POST'))
def _visual():

    '''
    result = wideip_ssh()

    for i in range(len(result)):
        wideip_data = L4_wideip.query.filter_by(wideip = result[i][0]).first()
        if(wideip_data):
            wideip_data.id = i + 1
            wideip_data.wideip_record = result[i][1]
            wideip_data.wideip_status = result[i][2]
            wideip_data.wideip_en = result[i][3]
            wideip_data.wideip_lbmod = result[i][4]
            wideip_data.wideip_rcof = result[i][5]
        else:
            comment = L4_wideip(id= i+1, wideip = result[i][0], wideip_record = result[i][1], wideip_status = result[i][2],
                                wideip_en = result[i][3], wideip_lbmod = result[i][4], wideip_rcof = result[i][5])
            db.session.add(comment)
        db.session.commit()
    '''
    result = 0

    #return render_template('visual/L4_visual.html', result = result, len=len(result))
    return render_template('visual/L4_visual.html', result = result)
    #return render_template('../static/visual.js', result = result)

@bp.route('/api/tree')
def get_tree_data():
    tree_data_temp = [
            {
                "id": 1,
                "label": "Parent",
                "children": [
                    {
                        "id": 2,
                        "label": "Child 1",
                        "attr1": "Attribute 1",
                        "attr2": "Attribute 2"
                    },
                    {
                        "id": 3,
                        "label": "Child 2",
                        "attr1": "Attribute 1",
                        "attr2": "Attribute 2"
                    }
                ]
            }
    ]

    return jsonify(tree_data)




@bp.route('/wideip/a')
def _wideip_a():
    #url = 'https://211.49.171.10/mgmt/tm/gtm/wideip/a'
    url = 'https://211.49.171.10/mgmt/tm/gtm/pool/cname/pool_c_admin-cf.img.afgslb.afreecatv.com/members/stats'
    data = get_data(url)
    return jsonify(data)

@bp.route('/pool/a')
def _pool_a():
    #url = 'https://211.49.171.10/mgmt/tm/gtm/pool/a/pool_bjapi.afgslb.afreecatv.com/members'
    #url = 'https://211.49.171.10/mgmt/tm/gtm/pool/a'
    url = 'https://211.49.171.10/mgmt/tm/gtm/pool/cname/pool_c_admin-cf.img.afgslb.afreecatv.com/members'
    data = get_data(url)
    return jsonify(data)


def get_data(url):
    auth = ('afguest', 'dk#mSLBguest')
    response = requests.get(url, auth=auth, verify=False)

    return response.text


'''
@bp.route('/visual', methods=('GET', 'POST'))
def _visual():
    #url = 'https://211.49.171.10/mgmt/tm/gtm/pool/a/pool_bjapi.afgslb.afreecatv.com/members'
    url = 'https://211.49.171.10/mgmt/tm/gtm/wideip/a'
    auth = ('afguest', 'dk#mSLBguest')
    response = requests.get(url, auth=auth, verify=False)

    return render_template('visual/L4_visual.html', result = response.text)
'''
