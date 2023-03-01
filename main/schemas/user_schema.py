# print(f'-------------------------------------{__name__}----------------------------------------------')

from extensions import marshmallow as ma
from main.models import User
from marshmallow import post_load, fields
from main.utilities import app_logger as logger


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True)

    # topics = fields.List(fields.Nested(topic_schema.TopicSchema))

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class LoginCredentials(ma.Schema):
    """
    marshmallow schema representing the email/token and password fields
    """
    email_token = fields.String(load_only=True)
    password = fields.String(required=False, load_only=True)
