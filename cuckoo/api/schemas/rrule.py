from marshmallow import fields

from .fields import FreqField, TimestampField
from .schedule import ScheduleSchema


class RRuleByField(fields.String):
    pass


class RRuleSchema(ScheduleSchema):
    freq = FreqField()
    dtstart = TimestampField(format='timestamp')
    interval = fields.Integer()
    wkst = fields.String()
    count = fields.Integer()
    until = fields.DateTime(allow_none=True)
    bysetpos = RRuleByField()
    bymonth = RRuleByField()
    bymonthday = RRuleByField()
    byyearday = RRuleByField()
    byeaster = RRuleByField()
    byweekno = RRuleByField()
    byweekday = RRuleByField()
    byhour = RRuleByField()
    byminute = RRuleByField()
    bysecond = RRuleByField()
