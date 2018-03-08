import re
from cached_property import cached_property
from sqlalchemy.orm import joinedload

from flask import request

from cuckoo.models import ApplicationApiToken
from cuckoo.exceptions import AuthenticationFailed


class Tenant(object):
    @classmethod
    def from_application(cls, application):
        if not application:
            return cls()

        return ApplicationTenant(application_id=application.id)


class ApplicationTenant(Tenant):
    def __init__(self, application_id):
        self.application_id = application_id

    def __repr__(self):
        return '<{} application_id={}>'.format(type(self).__name__, self.application_id)

    @cached_property
    def application_ids(self):
        if not self.application_id:
            return None
        return [self.application_id]


def get_tenant_from_token():
    header = request.headers.get('Authorization', '').lower()
    if not header:
        return None

    if not header.startswith('bearer'):
        return None

    token = re.sub(r"^bearer(:|\s)\s*", '', header).strip()
    parts = token.split('-')

    if not len(parts) == 3:
        raise AuthenticationFailed

    if parts[1] == 'a':
        return get_tenant_from_application_token(parts[2])

    raise AuthenticationFailed


def get_tenant_from_application_token(key):
    # .options(joinedload('user')) \
    token = ApplicationApiToken.query \
        .filter(ApplicationApiToken.key == key) \
        .first()

    if not token:
        raise AuthenticationFailed

    return Tenant.from_application(token.application)


def set_current_tenant(tenant):
    pass
