__all__ = ['Schedule']

import json

from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import JSON
from redbeat.decoder import RedBeatJSONDecoder, RedBeatJSONEncoder


def to_dict(schedule):
    return json.dumps(schedule, cls=RedBeatJSONEncoder)


def to_schedule(data):
    str_data = data
    return json.loads(str_data, cls=RedBeatJSONDecoder)


class Schedule(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        # way in -> DB
        if value is not None:
            return str(to_dict(value))
        return {}

    def process_result_value(self, value, dialect):
        # way out DB
        if value:
            return to_schedule(value)
        return None
