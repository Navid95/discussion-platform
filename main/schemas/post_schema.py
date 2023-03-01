# print(f'-------------------------------------{__name__}----------------------------------------------')

from marshmallow import fields, post_load, pre_load, post_dump
from main.models import Post
from main.schemas import BaseSchema
from extensions import marshmallow as ma
from main.utilities import app_logger as logger


class PostSchema(ma.SQLAlchemySchema, BaseSchema):
    name = 'post'

    class Meta:
        model = Post
        include_fk = True

    id = fields.Integer(dump_only=True)
    content = fields.String()
    topic_id = fields.Integer(dump_only=True)
    author_id = fields.Integer(dump_only=True)

    @post_load
    def make_post(self, data, many,**kwargs):
        return Post(**data)
