from secrets import token_hex

from sqlalchemy.ext.declarative import declared_attr

from cuckoo.db.types import GUID
from cuckoo.config import db


class StandardAttributes(object):
    created_at = db.Column(db.DateTime(True), default=db.func.now(),
                           nullable=False)

    @declared_attr
    def id(cls):
        return db.Column(GUID, primary_key=True, default=GUID.default_value)


class ApplicationBoundMixin(object):
    @declared_attr
    def application_id(cls):
        return db.Column(
            GUID, db.ForeignKey('application.id', ondelete='CASCADE'), nullable=False, index=True
        )

    @declared_attr
    def application(cls):
        return db.relationship('Application', innerjoin=True, uselist=False)


class ApiTokenMixin(object):
    @declared_attr
    def key(cls):
        return db.Column(
            db.String(64), default=lambda: ApiTokenMixin.generate_token(), unique=True, nullable=False
        )

    @classmethod
    def generate_token(cls):
        return token_hex(32)

    def get_token_key(self):
        raise NotImplementedError

    def get_tenant(self):
        raise NotImplementedError
