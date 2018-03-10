from .base import Resource

from cuckoo.config import db
from cuckoo.models import Job
from ..schemas import JobSchema

job_schema = JobSchema(strict=True)


class JobDetailsResource(Resource):
    def dispatch_request(self, job_id, *args, **kwargs):
        job = Job.query.get(job_id)
        if not job:
            return self.not_found()
        return Resource.dispatch_request(self, job, *args, **kwargs)

    def get(self, job):
        return self.respond_with_schema(job_schema, job)

    def delete(self, job):
        db.session.delete(job)
        db.session.commit()
        return self.respond(status=204)
