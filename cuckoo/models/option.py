from cuckoo.config import db
from cuckoo.db.types import GUID


class Option(db.Model):
    id = db.Column(GUID, primary_key=True, default=GUID.default_value)
    option_id = db.Column(GUID, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    value = db.Column(db.Text, nullable=False)

    __tablename__ = 'option'
    __table_args__ = (db.UniqueConstraint('option_id', 'name',
                                          name='unq_option_name'), )
