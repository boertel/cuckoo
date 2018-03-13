from sqlalchemy.dialects.postgresql import ARRAY, JSON
from cuckoo.config import db
from cuckoo.db.mixins import GUID
from cuckoo.db.mixins import StandardAttributes


class Identity(StandardAttributes, db.Model):
    user_id = db.Column(
        GUID, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False,
        index=True
    )
    external_id = db.Column(db.String(64), unique=True, nullable=False)
    provider = db.Column(db.String(32),  nullable=True)
    config = db.Column(JSON, nullable=False)
    scopes = db.Column(ARRAY(db.String(64)), nullable=True)

    user = db.relationship('User')

    __tablename__ = 'identity'
    __table_args__ = (db.UniqueConstraint(
        'user_id', 'provider', name='unq_identity_user'), )
