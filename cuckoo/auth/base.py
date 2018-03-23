from flask import session, g

from cuckoo.exceptions import AuthenticationFailed
from cuckoo.models import User
from .tenant import Tenant


def login_user(uid):
    set_tenant_for_session(uid)
    g.current_user = User.query.get(uid)


def get_current_user():
    current_user = getattr(g, 'current_user', None)
    if not current_user:
        current_user = get_user_from_request()
        g.current_user = current_user
    return current_user


def get_user_from_request():
    uid = session.get('uid', None)
    if not uid:
        return None
    return User.query.get(uid)




def get_current_tenant():
    current_tenant = getattr(g, 'current_tenant', None)
    if not current_tenant:
        current_tenant = get_tenant_from_request()
        set_current_tenant(current_tenant)
    return current_tenant


def get_tenant_from_request():
    #tenant = get_tenant_from_token()
    tenant = None   # TODO(boertel) handle api tenant
    if tenant:
        return tenant
    user = get_current_user()
    return Tenant.from_user(user)


def set_current_tenant(tenant):
    g.current_tenant = tenant


def set_tenant_for_session(uid):
    session['uid'] = uid
    session.permanent = True

