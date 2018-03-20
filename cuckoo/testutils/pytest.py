import os
import pytest

from sqlalchemy import event
from sqlalchemy.orm import Session

from cuckoo import config


@pytest.fixture(scope='session')
def session_config(request):
    return {
        'db_name': 'test_cuckoo',
    }


@pytest.fixture(scope='session')
def app(request, session_config):
    app = config.create_app(
        SQLALCHEMY_DATABASE_URI='postgresql://localhost/' + session_config['db_name'],
        SECRET_KEY=os.urandom(24),
        GITHUB_CLIENT_ID='github.client-id',
        GITHUB_CLIENT_SECRET='github.client-secret',
    )
    app.testing = True
    yield app


@pytest.fixture(scope='session', autouse=True)
def db(request, app, session_config):
    db_name = session_config['db_name']
    with app.app_context():
        assert not os.system('dropdb --if-exists %s' % db_name)
        assert not os.system('createdb -E utf-8 %s' % db_name)
        config.alembic.upgrade()
        return config.db


@pytest.fixture(scope='function')
def req_ctx(request, app):
    with app.test_request_context() as req_ctx:
        yield req_ctx


@pytest.fixture(scope='function', autouse=True)
def db_session(request, req_ctx, db):
    db.session.begin_nested()

    yield db.session


@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        yield client
