from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    email = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
