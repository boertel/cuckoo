from datetime import datetime

from marshmallow import fields


def timestampformat(timestamp, *args, **kwargs):
    dt = datetime.utcfromtimestamp(timestamp).replace(microsecond=0)
    return dt


def from_timestamp(timestampstr, *args, **kwargs):
    return timestampstr


class TimestampField(fields.DateTime):
    DATEFORMAT_SERIALIZATION_FUNCS = {
        **fields.DateTime.DATEFORMAT_SERIALIZATION_FUNCS,
        'timestamp': timestampformat,
    }

    DATEFORMAT_DESERIALIZATION_FUNCS = {
        **fields.DateTime.DATEFORMAT_DESERIALIZATION_FUNCS,
        'timestamp': from_timestamp,
    }
