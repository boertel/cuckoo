from flask import session, g

from cuckoo.models import User


def login_user(uid):
    set_tenant_for_session(uid)
    g.current_user = User.query.get(uid)


def get_current_user():
    return get_tenant_from_session()


def set_tenant_for_session(uid):
    session['uid'] = uid
    session.permanent = True


def get_tenant_from_session():
    uid = session['uid']
    return User.query.get(uid)
