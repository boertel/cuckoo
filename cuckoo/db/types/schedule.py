__all__ = ['Schedule']


from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import JSON

from cuckoo.utils.redbeat import from_schedule_to_dict, from_dict_to_schedule


class Schedule(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        # way in -> DB
        if value is not None:
            return str(from_schedule_to_dict(value))
        return {}

    def process_result_value(self, value, dialect):
        # way out DB
        if value:
            return from_dict_to_schedule(value)
        return None
