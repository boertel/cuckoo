from marshmallow import fields

from . import ScheduleSchema


class IntervalSchema(ScheduleSchema):
    every = fields.Integer()
    relative = fields.Boolean(default=False, missing=False)
