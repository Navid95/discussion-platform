print(f'-------------------------------------{__name__}-------------------------------------')

from flask import request, jsonify, abort
from ...models import User
from ...schemas import user_schema
import main.authentication as authentication
from . import user

from log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)

api = user
schema = user_schema.UserSchema()
auth = authentication.auth
"""
CRUD APIs
"""


# TODO remove this API
@api.route('/get/all', methods=['GET'])
def get_all():
    return schema.dumps(User.get_all(), many=True)


@api.route('/<id>', methods=['GET'])
@authentication.user_owner_required
def get_instance(id):
    return schema.dumps(User.get_instance(id=id))


@api.route('/', methods=['GET'])
@authentication.user_owner_required
def search_user(id):
    """
    Search API with URI string filters
    :param id:
    :return:
    """
    pass


@api.route('/', methods=['POST'])
def create_user():
    json_raw = request.get_json()
    create_user = schema.load(json_raw)
    result = User.persist(create_user)
    if result:
        return schema.dumps(create_user)
    else:
        abort(400)


@api.route('/', methods=['PUT', 'PATCH'])
def update_user():
    pass


@api.route('/delete', methods=['DELETE'])
def delete_user():
    pass


@api.before_app_request
@auth.login_required
def before_request():
    logger.debug(f'before_app_request for request: {request}')
