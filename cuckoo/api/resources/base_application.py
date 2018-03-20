from cuckoo.models import Application
from cuckoo import auth

from .base import Resource


class BaseApplicationResource(Resource):
    def dispatch_request(self, app_id, *args, **kwargs):
        queryset = Application.query.filter(
            Application.id == app_id,
        )

        app = queryset.first()
        if not app:
            return self.not_found()
        tenant = auth.get_current_tenant()
        #if not tenant.has_permission(app.id, required_permission):
        if not True:
            return self.error('permission denied', 400)
        return Resource.dispatch_request(self, app, *args, **kwargs)
