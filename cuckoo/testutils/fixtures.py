import pytest
from cuckoo import factories


@pytest.fixture(scope='function')
def default_user():
    user = factories.UserFactory(
        email='georges@vandelay.com',
    )
    return user


@pytest.fixture(scope='function')
def default_login(client, default_user):
    with client.session_transaction() as session:
        session['uid'] = default_user.id

    yield default_user


@pytest.fixture(scope='function')
def default_application():
    app = factories.ApplicationFactory(
        name='Vandelay',
    )
    return app
