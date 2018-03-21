from redbeat import RedBeatSchedulerEntry
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import JSON

from cuckoo.config import db, celery
from cuckoo.db.types import Schedule
from cuckoo.db.mixins import StandardAttributes, ApplicationBoundMixin


class Job(StandardAttributes, ApplicationBoundMixin, db.Model):
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    params = db.Column(JSON)
    schedule = db.Column(Schedule)
    enabled = db.Column(db.Boolean, default=False)

    __tablename__ = 'job'

    def get_redis_key(self):
        return 'redbeat:{}'.format(str(self.id))


@event.listens_for(Job, 'after_insert')
def create_task(mapper, connection, target):
    assert target.id is not None
    # TODO(boertel) somehow target isn't the object from the database and the
    # deserialization of schedule isn't done
    job = Job.query.filter_by(id=target.id).first()
    if job:
        celery_app = celery.get_celery_app()
        task_name = 'cuckoo.tasks.webhook.webhook'
        args = [
            str(job.id),
            str(job.application_id),
        ]
        kwargs = {
            'url': job.url,
            'data': job.params,
        }
        entry = RedBeatSchedulerEntry(str(job.id),
                                      task_name,
                                      job.schedule,
                                      args=args,
                                      kwargs=kwargs,
                                      app=celery_app,
                                      )
        entry.save()


@event.listens_for(Job, 'after_delete')
def delete_task(mapper, connection, target):
    celery_app = celery.get_celery_app()
    entry = RedBeatSchedulerEntry.from_key(target.get_redis_key(), celery_app)
    entry.delete()


@event.listens_for(Job, 'after_update')
def update_task(mapper, connection, target):
    pass
