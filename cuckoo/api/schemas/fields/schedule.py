import json
from marshmallow import fields
from redbeat.decoder import RedBeatJSONDecoder, RedBeatJSONEncoder


def to_dict(schedule):
    return json.dumps(schedule, cls=RedBeatJSONEncoder)


def to_schedule(data):
    str_data = data
    return json.loads(str_data, cls=RedBeatJSONDecoder)


class ScheduleField(fields.Nested):
    def __init__(self, schedule_mapping, *args, **kwargs):
        self.schedule_mapping = schedule_mapping
        nested = list(schedule_mapping.values())[0]
        super().__init__(nested, *args, **kwargs)

    def get_schema(self, value):
        return self.schedule_mapping.get(value, self.nested)

    def _serialize(self, value, attr, obj):
        # value is a obj
        response = json.loads(to_dict(obj.schedule))
        self.nested = self.get_schema(response['__type__'])
        return super()._serialize(response, attr, obj)

    def _deserialize(self, value, attr, data):
        # value is a dict
        self.nested = self.get_schema(value['type'])
        response = super()._deserialize(value, attr, data)
        return to_schedule(json.dumps(response))
