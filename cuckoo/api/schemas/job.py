import json
from marshmallow import Schema, fields, post_load
from redbeat.decoder import RedBeatJSONDecoder, RedBeatJSONEncoder

from cuckoo.models import Job


class ScheduleSchema(Schema):
    __type__ = fields.String(load_from='type', dump_to='type')


class IntervalSchema(ScheduleSchema):
    every = fields.Integer()
    relative = fields.Boolean(default=False)


class CrontabSchema(ScheduleSchema):
    minute = fields.String()
    hour = fields.String()
    day_of_week = fields.String()
    day_of_month = fields.String()
    month_of_year = fields.String()


class DatetimeSchema(ScheduleSchema):
    pass


class RRuleSchema(ScheduleSchema):
    pass


SCHEMAS_MAPPING = {
    'interval': IntervalSchema,
    'crontab': CrontabSchema,
}


class ScheduleField(fields.Nested):
    def _serialize(self, value, attr, obj):
        # value is a str
        print('\n--------- _serialize', value, '\n')
        response = json.loads(json.dumps(obj.schedule, cls=RedBeatJSONEncoder))
        self.nested = SCHEMAS_MAPPING.get(response['__type__'])
        return super()._serialize(response, attr, obj)

    def _deserialize(self, value, attr, data):
        # value is a dict
        print('\n--------- _deserialize', value, '\n')
        self.nested = SCHEMAS_MAPPING.get(value['type'])
        return super()._deserialize(value, attr, data)


class JobSchema(Schema):
    id = fields.UUID(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    name = fields.Str()
    url = fields.Url()
    schedule = ScheduleField(IntervalSchema)
    enabled = fields.Bool()

    @post_load
    def make_job(self, data):
        return Job(**data)
