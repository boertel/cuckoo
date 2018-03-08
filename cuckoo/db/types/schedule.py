__all__ = ['Schedule']

import json

from sqlalchemy.types import TypeDecorator, Unicode
from redbeat.decoder import RedBeatJSONDecoder, RedBeatJSONEncoder
from flask import current_app


def to_dict(schedule):
    return json.dumps(schedule, cls=RedBeatJSONEncoder)


def to_schedule(data):
    str_data = data
    return json.loads(str_data, cls=RedBeatJSONDecoder)


class Schedule(TypeDecorator):
    impl = Unicode

    def process_bind_param(self, value, dialect):
        # way in -> DB
        #current_app.logger.info('process_bind_param', value)
        if value is not None:
            return str(to_dict(value))
        return '{}'

    def process_result_value(self, value, dialect):
        # way out DB
        #current_app.logger.info('process_result_value', value)
        if value:
            return to_schedule(value)
        return None
