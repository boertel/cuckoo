from cuckoo.config import db
from cuckoo.models import Job

from .base import Resource
from ..schemas import JobSchema

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)


class JobIndexResource(Resource):
    def get(self, application):
        jobs = Job.query.filter_by(application=application)
        return self.respond_with_schema(jobs_schema, jobs)

    def post(self, application):
        result = self.schema_from_request(job_schema)
        if result.errors:
            return self.respond(result.errors, 403)
        job = result.data
        job.application = application
        db.session.add(job)
        db.session.commit()

        return self.respond_with_schema(job_schema, job)
