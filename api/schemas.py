from marshmallow import Schema, fields,post_load
from api.models import User


class TaskSchema(Schema):
  id = fields.Str(required=True)
  title = fields.Str()
  description = fields.Str()
  done = fields.Bool()


class UserSchema(Schema):
    _id = fields.Str(required=True)
    username = fields.Str()
    password = fields.Str()
    admin = fields.Bool()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)