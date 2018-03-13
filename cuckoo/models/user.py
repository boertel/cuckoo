from cuckoo.config import db
from cuckoo.db.mixins import StandardAttributes


class User(StandardAttributes, db.Model):
    email = db.Column(db.String(128), unique=True, nullable=False)

    options = db.relationship(
        'Option',
        foreign_keys='[Option.option_id]',
        primaryjoin='Option.option_id == User.id',
        viewonly=True,
        uselist=True
    )

    __tablename__ = 'user'
