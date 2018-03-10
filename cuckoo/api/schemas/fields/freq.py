from redbeat.schedules import rrule
from marshmallow import fields


FREQ_INT_TO_STR = {v: k for k, v in rrule.FREQ_MAP.items()}
FREQ_STR_TO_INT = rrule.FREQ_MAP


class FreqField(fields.Integer):
    def _serialize(self, value, attr, obj):
        return FREQ_INT_TO_STR[value]

    def _deserialize(self, value, attr, obj):
        return FREQ_STR_TO_INT[value]
