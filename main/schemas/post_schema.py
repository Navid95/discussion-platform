print(f'-------------------------------------{__name__}----------------------------------------------')

from extensions import marshmallow as ma
from ..models import Post
import logging
from main.utilities import app_logger as logger


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        include_fk = True

    id = ma.auto_field()
    content = ma.auto_field()
    topic_id = ma.auto_field()
    author_id = ma.auto_field()
