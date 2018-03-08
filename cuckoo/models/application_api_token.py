from cuckoo.config import db
from cuckoo.db.mixins import ApiTokenMixin, StandardAttributes
from cuckoo.db.types import GUID
from cuckoo.db.utils import model_repr


class ApplicationApiToken(StandardAttributes, db.Model, ApiTokenMixin):
    application_id = db.Column(
        GUID, db.ForeignKey('application.id', ondelete='CASCADE'), nullable=False, unique=True
    )

    application = db.relationship(
        'Application', backref=db.backref('token', uselist=False), innerjoin=True
    )

    __tablename__ = 'application_api_token'
    __repr__ = model_repr('application_id', 'key')

    def get_token_key(self):
        return 'a'

    def get_tenant(self):
        self.user
