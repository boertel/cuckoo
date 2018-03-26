import maya
from marshmallow import fields


class MayaField(fields.Field):
    def _serialize(self, value, attr, obj):
        # when serializing after an api call json representation of schedule rrule
        # value/obj.dtstart is int:timestamp
        #return maya.MayaDT.from_datetime(value).iso8601()
        return maya.MayaDT(value).iso8601()

    def _deserialize(self, value, attr, data):
        return maya.when(value).epoch
