from functools import wraps
from main.schemas import UserSchema
from main.models import User
from flask import g, request
from main.utilities import app_logger as logger

schema = UserSchema()


def dump_user(f):
    """
    Serializes the return value of the decorated function with the marshmallow schema related to User model

    :param f: function to wrap, probably a view function
    :return: reference to the wrapper func that dumps the user obj with marshmallow schema
    """
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
