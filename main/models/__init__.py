from .post import Post
from .topic import Topic
from .user import User


from log_utils import init_logger
import logging
init_logger(__name__)
logger = logging.getLogger(__name__)

# TODO create base class for all models
