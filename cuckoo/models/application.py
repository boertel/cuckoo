from secrets import token_hex

from cuckoo.config import db
from cuckoo.db.utils import model_repr
from cuckoo.db.mixins import StandardAttributes
from cuckoo.db.types import GUID


class Application(StandardAttributes, db.Model):
    name = db.Column(db.String(200), nullable=False)
    client_id = db.Column(
        db.String(64), default=lambda: Application.generate_token(10),
        nullable=False, unique=True)
    client_secret = db.Column(
        db.String(64), default=lambda: Application.generate_token(),
        nullable=False, unique=True)

    jobs = db.relationship('Job', backref='jobs', lazy=True)

    user_id = db.Column(
        GUID,
        db.ForeignKey('user.id'), primary_key=True, unique=True
    )
    user = db.relationship('User', innerjoin=True, uselist=False)

    __tablename__ = 'application'
    __repr__ = model_repr('name', 'client_id')

    @classmethod
    def generate_token(cls, size=32):
        return token_hex(size)
