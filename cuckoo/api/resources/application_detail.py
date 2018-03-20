from cuckoo.config import db
from cuckoo import auth
from cuckoo.models import Application

from .base import Resource
from ..schemas import ApplicationSchema

application_schema = ApplicationSchema(strict=True)


class ApplicationDetailResource(Resource):
    def get(self, app_id):
        user = auth.get_current_user()
        application = Application.query.filter(Application.id == app_id, Application.user_id == user.id).first()
        return self.respond_with_schema(application_schema, application)
