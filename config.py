import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True
ITS_DANGEROUS_SECRET_KEY = 'abc'
