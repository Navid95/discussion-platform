import main.models as models
from marshmallow import post_load, fields
from main import marshmallow as ma
from . import topic_schema

import logging
from log_utils import init_logger

init_logger(__name__)
logger = logging.getLogger(__name__)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = models.User

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True)

    topics = fields.List(fields.Nested(topic_schema.TopicSchema))

    @post_load
    def make_user(self, data, **kwargs):
        return models.User(**data)
