from flask import session, g

from cuckoo.exceptions import AuthenticationFailed
from cuckoo.models import User


def login_user(uid):
    set_tenant_for_session(uid)
    g.current_user = User.query.get(uid)


def get_current_user():
    current_user = getattr(g, 'current_user', None)
    if not current_user:
        current_user = get_user_from_request()
        g.current_user = current_user
    return current_user


def get_current_tenant():
    return getattr(g, 'current_tenant', None)

def set_current_tenant(tenant):
    g.current_tenant = tenant


def set_tenant_for_session(uid):
    session['uid'] = uid
    session.permanent = True


def get_user_from_request():
    uid = session.get('uid', None)
    if not uid:
        return None
    return User.query.get(uid)
