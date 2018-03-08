from cuckoo.config import db

from .base import Resource
from ..schemas import ApplicationSchema

application_schema = ApplicationSchema(strict=True)


class ApplicationIndexResource(Resource):
    def post(self):
        result = self.schema_from_request(application_schema)
        if result.errors:
            self.respond(result.errors, 403)
        application = result.data
        db.session.add(application)
        db.session.commit()

        return self.respond_with_schema(application_schema, application)
