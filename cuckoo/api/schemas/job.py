from marshmallow import Schema, fields, post_load

from cuckoo.models import Job

from .rrule import RRuleSchema
from .crontab import CrontabSchema
from .interval import IntervalSchema
from .fields import ScheduleField


SCHEDULE_MAPPING = {
    'interval': IntervalSchema,
    'crontab': CrontabSchema,
    'rrule': RRuleSchema,
}


class JobSchema(Schema):
    id = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    name = fields.Str()
    url = fields.Url()
    schedule = ScheduleField(schedule_mapping=SCHEDULE_MAPPING)
    enabled = fields.Bool()

    @post_load
    def make_job(self, data):
        return Job(**data)
