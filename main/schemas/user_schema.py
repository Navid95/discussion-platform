print(f'-------------------------------------{__name__}----------------------------------------------')

from ..extensions import marshmallow as ma
from ..models import User
from marshmallow import post_load, fields
import logging
from log_utils import init_logger

init_logger(__name__)
logger = logging.getLogger(__name__)


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
