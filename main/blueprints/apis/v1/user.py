import main.blueprints.apis.v1 as api_version
import logging
from log_utils import init_logger
import main.models.user as model
from flask import request, jsonify, abort
import main.schemas as schemas
import main.authentication as authentication

init_logger(__name__)
logger = logging.getLogger(__name__)

api = api_version.apiv1
User = model.User
schema = schemas.user_schema.UserSchema()
auth = authentication.auth
"""
CRUD APIs
"""


# TODO remove this API
@api.route('/user/get/all', methods=['GET'])
def get_all():
    return schema.dumps(User.get_all(), many=True)


@api.route('/user/<id>', methods=['GET'])
@authentication.user_owner_required
def get_instance(id):
    return schema.dumps(User.get_instance(id=id))


@api.route('/user', methods=['GET'])
@authentication.user_owner_required
def search_user(id):
    """
    Search API with URI string filters
    :param id:
    :return:
    """
    pass


@api.route('/user', methods=['POST'])
def create_user():
    json_raw = request.get_json()
    create_user = schema.load(json_raw)
    result = User.persist(create_user)
    if result:
        return schema.dumps(create_user)
    else:
        abort(400)


@api.route('/user', methods=['PUT', 'PATCH'])
def update_user():
    pass


@api.route('/delete', methods=['DELETE'])
def delete_user():
    pass


@api.before_app_request
@auth.login_required
def before_request():
    logger.debug(f'before_app_request for request: {request}')
