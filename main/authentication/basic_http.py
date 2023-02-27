from flask import g, abort
from flask_httpauth import HTTPBasicAuth
from main.models import User
from functools import wraps

from main.configuration.log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)

auth = HTTPBasicAuth()


# TODO develop login module(redis, token generation for each user login)


@auth.verify_password
def verify_password(email, password):
    logger.debug(f'verifying password for {email}')
    if email == '':
        return False
    user = User.get_instance(email=email)
    if not user:
        return False
    elif user.verify_password(password):
        g.current_user = user
        return user
    else:
        return False


def user_owner_required(f):
    logger.debug(f'decorator user_owner_required intercepted request of {f.__name__}')

    @wraps(f)
    def decorated_func(*args, **kwargs):
        logger.debug(f'{decorated_func.__name__} received *args: {args} and **kwargs: {kwargs}')
        id = kwargs['id']
        logger.debug(f'{decorated_func.__name__} has g.current_user: {g.current_user}')
        if int(g.current_user.id) == int(id):
            logger.debug(f'{decorated_func.__name__} g.current_user: {g.current_user} == {kwargs["id"]}')
            return f(*args, **kwargs)
        else:
            abort(401)
    return decorated_func
