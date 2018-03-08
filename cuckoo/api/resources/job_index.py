from cuckoo.config import db
from cuckoo.models import Application

from .base import Resource
from ..schemas import JobSchema

job_schema = JobSchema()


class JobIndexResource(Resource):
    def post(self):
        result = self.schema_from_request(job_schema)
        if result.errors:
            return self.respond(result.errors, 403)
        job = result.data
        job.application = Application.query.all()[0]
        db.session.add(job)
        db.session.commit()

        return self.respond_with_schema(job_schema, job)
