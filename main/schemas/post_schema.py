print(f'-------------------------------------{__name__}----------------------------------------------')

from ..extensions import marshmallow as ma
from ..models import Post
import logging
from log_utils import init_logger

init_logger(__name__)
logger = logging.getLogger(__name__)


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        include_fk = True

    id = ma.auto_field()
    content = ma.auto_field()
    topic_id = ma.auto_field()
    author_id = ma.auto_field()
