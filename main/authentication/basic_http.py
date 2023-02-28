from flask import g, abort
from flask_httpauth import HTTPBasicAuth
from main.models import User
from functools import wraps
from . import token_auth
from main.utilities import app_logger as logger

auth = HTTPBasicAuth()


# TODO develop login module(redis, token generation for each user login)

@auth.verify_password
def verify_password(email, password_or_token):
    """
    verifies user credentials, if no email is provided fails immediately otherwise first checks token based authentication
    if no token is found drops to basic authentication (email & password)

    :param email: user account email
    :param password_or_token: token string or simple password of the account
    :return: user object in success and aborts(401) on failure
    """
    if email == '':
        logger.debug(f'no email provided, abort(401)')
        abort(401)
    else:
        logger.debug(f'authenticating user with email: {email} ...')
        user = User.get_instance(email=email)
        if not user:
            logger.debug(f'no user found with email: {email}, abort(401)')
            abort(401)
        else:
            logger.debug(f'user found with email: {email}, trying token authentication')
            if token_auth.check_token(user.id,password_or_token):
                logger.debug(f'user authenticated with email: {email}, token authentication successful')
                g.current_user = user
                g.token_auth = True
                return user
            else:
                logger.debug(f'token not found with email: {email}, trying password authentication')
                if user.verify_password(password_or_token):
                    logger.debug(f'user authenticated with email: {email}, password authentication successful')
                    g.current_user = user
                    g.token_auth = False
                    return user
                else:
                    logger.debug(f'wrong password for user with email: {email}, password authentication failed, abort(401)')
                    abort(401)


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
            logger.warning('not the owner of the user')
            abort(401)
            # return False

    return decorated_func
