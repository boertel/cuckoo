from cuckoo import auth


class ApiTokenAuthentication(object):
    def authenticate(self):
        return True


class SessionAuthentication(object):
    def authenticate(self):
        return auth.get_tenant_from_session()
