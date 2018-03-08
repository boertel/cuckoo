from .base import Resource

from cuckoo.models import Job
from ..schemas import JobSchema

job_schema = JobSchema(strict=True)


class JobDetailsResource(Resource):
    def get(self, job_id):
        job = Job.query.get(job_id)
        return self.respond_with_schema(job_schema, job)
