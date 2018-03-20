from flask import g

from cuckoo.config import db
from cuckoo import auth
from cuckoo.models import Application

from .base import Resource
from ..schemas import ApplicationSchema

application_schema = ApplicationSchema(strict=True)
applications_schema = ApplicationSchema(strict=True, many=True)


class ApplicationIndexResource(Resource):
    def get(self):
        current_user = g.current_user
        applications = Application.query.filter(Application.user_id == current_user.id)
        return self.respond_with_pagination(applications_schema, applications)

    def post(self):
        result = self.schema_from_request(application_schema)
        if result.errors:
            self.respond(result.errors, 403)
        application = result.data
        application.user = g.current_user
        if db.session.is_modified(application):
            db.session.add(application)
            db.session.commit()
        return self.respond_with_schema(application_schema, application)
