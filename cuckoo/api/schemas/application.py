from marshmallow import Schema, fields, post_load

from cuckoo.models import Application


class ApplicationSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    client_id = fields.Str(dump_only=True)

    @post_load
    def make_application(self, data):
        return Application(**data)
