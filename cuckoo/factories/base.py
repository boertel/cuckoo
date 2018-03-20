from sqlalchemy.orm.scoping import scoped_session
from factory import alchemy

from flask import current_app


def get_my_session():
    return current_app.extensions['sqlalchemy'].db.session


class ModelFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = scoped_session(get_my_session)
