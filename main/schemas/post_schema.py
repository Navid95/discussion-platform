# print(f'-------------------------------------{__name__}----------------------------------------------')

from extensions import marshmallow as ma
from marshmallow import fields, post_load
from main.models import Post
import logging
from main.utilities import app_logger as logger


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        include_fk = True

    id = fields.Integer(dump_only=True)
    content = fields.String()
    topic_id = fields.Integer(dump_only=True)
    author_id = fields.Integer(dump_only=True)

    @post_load
    def make_post(self, data,**kwargs):
        return Post(**data)
