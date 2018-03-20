from cuckoo import auth


class ApiTokenAuthentication(object):
    def authenticate(self):
        return True


class SessionAuthentication(object):
    def authenticate(self):
        user = auth.get_current_user()
        if not user:
            return None
        return auth.Tenant.from_user(user)
