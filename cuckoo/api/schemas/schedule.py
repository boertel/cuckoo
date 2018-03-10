from marshmallow import Schema, fields


class ScheduleSchema(Schema):
    __type__ = fields.String(load_from='type', dump_to='type')
