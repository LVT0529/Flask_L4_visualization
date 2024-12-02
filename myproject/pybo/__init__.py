from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_sslify import SSLify


import config


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()



def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    #ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from . import models


    #블루프린트
    from .views import main_views, question_views, answer_views, auth_views, comment_views, GSLB_visual_views, network_report_views, slb_views, switch_views, slb_config, ipinfo_views
    from .views.SLB import afmainslb_5F_views, afimgslb_B2F_views, afreecaslb_5F_views, nowlximgslb_5F_views, afahvslb1_4F_views, afahvslb3_4F_views, afahvslb5_4F_views, kidcslb_B2F_views, nliveimgslb_B2F_views, integrated_slb_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(GSLB_visual_views.bp)
    app.register_blueprint(network_report_views.bp)
    app.register_blueprint(afmainslb_5F_views.bp)
    app.register_blueprint(afimgslb_B2F_views.bp)
    app.register_blueprint(afreecaslb_5F_views.bp)
    app.register_blueprint(nowlximgslb_5F_views.bp)
    app.register_blueprint(afahvslb1_4F_views.bp)
    app.register_blueprint(afahvslb3_4F_views.bp)
    app.register_blueprint(afahvslb5_4F_views.bp)
    app.register_blueprint(kidcslb_B2F_views.bp)
    app.register_blueprint(nliveimgslb_B2F_views.bp)
    app.register_blueprint(slb_views.bp)
    app.register_blueprint(switch_views.bp) 
    app.register_blueprint(slb_config.bp)
    app.register_blueprint(ipinfo_views.bp)
    app.register_blueprint(integrated_slb_views.bp)

    #필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime


    return app

