import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = b'\x9f\x82\xe6\xed:\xcf\xdbR\x07\xc0\x14\xd1\xd1X\xe9s'
