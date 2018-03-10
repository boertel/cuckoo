from marshmallow import fields

from .schedule import ScheduleSchema


class CrontabSchema(ScheduleSchema):
    minute = fields.String()
    hour = fields.String()
    day_of_week = fields.String()
    day_of_month = fields.String()
    month_of_year = fields.String()
