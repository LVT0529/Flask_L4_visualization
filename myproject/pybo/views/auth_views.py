import functools

from flask import Flask, Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

from flask_ldap3_login import LDAP3LoginManager,AuthenticationResponseStatus
from ldap3 import Server, Connection


import logging



app = Flask(__name__)

app.config['LDAP_HOST'] = 'dc.office.afreecatv.com'  # LDAP 서버 주소
app.config['LDAP_BASE_DN'] = 'DC=office,DC=afreecatv,DC=com'  # 기본 검색 베이스 DN
# `LDAP_USER_DN` 설정은 해당 사용자가 위치한 OU 경로를 지정합니다.
# 여기서는 사용자 인증 시 필요하지 않으므로 생략하거나, 모든 사용자가 공통적으로 위치한 가장 하위 OU를 지정합니다.
app.config['LDAP_USER_DN'] = 'OU=아프리카TV 조직, OU=TL부문,OU=인프라랩,OU=네트워크팀'
app.config['LDAP_PORT'] = 389  # LDAP 서버 포트, SSL을 사용하지 않는 경우 기본값은 389입니다.
app.config['LDAP_USE_SSL'] = False  # SSL 사용 여부, 여기서는 사용하지 않음으로 설정



ldap_manager = LDAP3LoginManager(app)



bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        #AD 인증 허용 유저 list
        username_list = {"dhkim": "김 동혁", "victory": "이 빅토", "jint": "진 태용", "gladday12": "김 효진", "khpkim": "김 형필", "snaghoon": "이 상훈",
        "callsign": "이 승회", "zndkddl": "김 병모", "jeonghk": "샤를_정홍규", "kataehan159": "가 태한", "jsjee": "지 정수", "jungin.kwon": "권 정인",
        "joan": "조 유정", "creras1004":"하 창완"}

        username = username_list.get(username)

        if (username in ("가 태한", "지 정수", "권 정인", "조 유정", "하 창완")):
            user_dn = f"CN={username},OU=시스템팀,OU=인프라랩,OU=TL부문,OU=아프리카TV 조직,DC=office,DC=afreecatv,DC=com"
        else:
            user_dn = f"CN={username},OU=네트워크팀,OU=인프라랩,OU=TL부문,OU=아프리카TV 조직,DC=office,DC=afreecatv,DC=com"
        #user_dn = f"CN={username},OU=네트워크팀,OU=인프라랩,OU=TL부문,OU=아프리카TV 조직,DC=office,DC=sooplive,DC=com"
        user = None
        server = Server(app.config['LDAP_HOST'], port=app.config['LDAP_PORT'], use_ssl=app.config['LDAP_USE_SSL'])
        connection = Connection(server, user=user_dn, password=password)
        if connection.bind():
            # AD authentication successful
            # Set user session based on AD authentication result
            session.clear()

            user = User.query.filter_by(username=username).first()

            if not user:
                user = User(username=username, password=None, email=None)
                db.session.add(user)
                db.session.commit() 
            session['user_id'] = user.id
            return redirect(url_for('main.list'))
        else:
            flash('AD 인증 실패.')

    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view
