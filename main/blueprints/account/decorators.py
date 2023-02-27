from functools import wraps
from main.schemas import UserSchema
from main.models import User
from flask import g, request

from main.configuration.log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)
schema = UserSchema()


def dump_user(f):
    @wraps(f)
    def wrap_dump_user(*args, **kwargs):
        logger.debug(f'processing response of {f.__name__}')
        value = f(*args, **kwargs)
        return schema.dumps(value)

    return wrap_dump_user


# TODO check if we can do deserialization with decorators
def load_user(f):
    @wraps(f)
    def wrap_load_user(*args, **kwargs):
        value = f(*args, **kwargs)
        return value

    return f
