from cuckoo import auth
from cuckoo.models import User

from .base import Resource
from ..schemas import UserSchema

user_schema = UserSchema()


class UserDetailResource(Resource):
    def get(self, user_id):
        if user_id == 'me':
            user = auth.get_current_user()
        else:
            user = User.query.get(user_id)
        return self.respond_with_schema(user_schema, user)
