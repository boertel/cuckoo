import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

from cuckoo.utils.celery import Celery


alembic = Alembic()
celery = Celery()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    SQLALCHEMY_URI = os.environ.get('SQLALCHEMY_URI')
    REDIS_URL = os.environ.get('REDIS_URL')

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['REDIS_URL'] = REDIS_URL

    app.config['CELERY_BORKER_URL'] = REDIS_URL

    app.config['CELERY_ACCEPT_CONTENT'] = ['json']
    app.config['CELERY_ACKS_LATE'] = True
    app.config.setdefault('CELERY_BROKER_URL', app.config['REDIS_URL'])
    app.config['CELERY_TASK_SERIALIZER'] = 'json'
    # app.config['CELERY_IMPORTS'] = ('cuckoo.tasks', )
    app.config['CELERY_INCLUDE'] = ('cuckoo.tasks', )
    app.config['CELERY_IGNORE_RESULT'] = True
    app.config['CELERY_RESULT_BACKEND'] = None
    # dont let tasks run more than 5 minutes
    app.config['CELERY_TASK_SOFT_TIME_LIMIT'] = 300
    app.config['TIMEZONE'] = 'UTC'
    # hard kill after 6 minutes
    app.config['CELERY_TASK_TIME_LIMIT'] = 360

    app.config['CELERYBEAT_SCHEDULE'] = {
    }

    app.config['REDBEAT_REDIS_URL'] = app.config['REDIS_URL']

    configure_db(app)

    celery.init_app(app)

    configure_api(app)

    from . import models #NOQA

    return app


def configure_db(app):
    alembic.init_app(app)
    db.init_app(app)


def configure_api(app):
    from cuckoo import api
    app.register_blueprint(api.app, url_prefix='/api')
