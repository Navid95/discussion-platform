from functools import wraps
from flask import g, request, abort
from .jwt_extended import jwt
from main.models import User, Topic, Post
from main.utilities import app_logger as logger,NoUserFound
from flask_jwt_extended import current_user
from main.schemas import LoginSchema

login_schema = LoginSchema()


def load_login_data(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = login_schema.load(request.get_json())
        g.input_data = data
        value = f(*args, **kwargs)
        return value
    return wrapper


def validate_login_credentials_post(email, password):
    user = User.get_instance(email=email)
    if user is not None:
        if user.verify_password(password):
            g.current_user = user
            return True
        else:
            raise NoUserFound('Password authentication failed for given email')
    else:
        raise NoUserFound('No user found with given email')

def user_owner_required(f):
    logger.debug(f'decorator user_owner_required intercepted request of {f.__name__}')

    @wraps(f)
    def decorated_func(*args, **kwargs):
        id = kwargs['id']
        if int(current_user.id) == int(id):
            logger.debug(f'{decorated_func.__name__} current_user: {current_user} == {kwargs["id"]}')
            return f(*args, **kwargs)
        else:
            logger.warning('not the owner of the user')
            abort(401)
            # return False

    return decorated_func


def topic_owner_required(f):

    @wraps(f)
    def check_owner(*args, **kwargs):
        topic_id = kwargs['topic_id']
        if current_user.owns_topic(Topic.get(topic_id)):
            logger.debug(f'{check_owner.__name__} current_user: {current_user} owns Topic id: {topic_id}')
            return f(*args, **kwargs)
        else:
            logger.warning('not the owner of the topic')
            abort(401)

    return check_owner


def post_owner_required(f):

    @wraps(f)
    def check_owner(*args, **kwargs):
        post_id = kwargs['post_id']
        if current_user.owns_post(Post.get(post_id)):
            logger.debug(f'{check_owner.__name__} current_user: {current_user} owns Post id: {post_id}')
            return f(*args, **kwargs)
        else:
            logger.warning('not the owner of the post')
            abort(401)

    return check_owner


