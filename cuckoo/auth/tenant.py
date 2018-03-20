from cached_property import cached_property
from flask import g

from cuckoo.models import Application, db


class Tenant(object):
    def get_permission(self, application_id):
        pass

    def has_permission(self, application_id):
        pass

    def access(self):
        raise NotImplementedError

    @classmethod
    def from_application(cls, application):
        if not application:
            return cls()
        return ApplicationTenant(application_id=application.id)

    @classmethod
    def from_user(cls, user):
        if not user:
            return cls()
        g.current_user = user
        return UserTenant(user_id=user.id)


class ApplicationTenant(Tenant):
    def __init__(self, application_id):
        self.application_id = application_id

    @cached_property
    def access(self):
        if not self.application_id:
            return None
        return [self.application_id]


class UserTenant(Tenant):
    def __init__(self, user_id):
        self.user_id = user_id

    @cached_property
    def access(self):
        if not self.user_id:
            return None
        return db.session.query(Application.id).filter(Application.user_id == self.user_id)
