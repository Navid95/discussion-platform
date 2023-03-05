# print(f'-------------------------------------{__name__}----------------------------------------------')

from flask import g, jsonify, request, abort
from main.models import User, Topic, Post
from main.authentication import jwt, topic_owner_required
from flask_jwt_extended import jwt_required, current_user
from main.schemas import TopicSchema, PostSchema
from . import topic as api, decorators


schema = TopicSchema()
post_schema = PostSchema()
owner_required = topic_owner_required
dump_topic = decorators.dump_topic


@api.route('/', methods=['POST'])
@jwt_required()
@dump_topic
def init_topic():
    topic = schema.load(request.get_json())
    g.current_user = current_user
    if g.current_user.init_topic(topic):
        return topic
    else:
        return jsonify({'message': 'Something wrong happened'})


@api.route('/<topic_id>/follow', methods=['GET'])
@jwt_required()
@dump_topic
def follow_topic(topic_id):
    g.current_user = current_user
    topic = Topic.get(topic_id)
    if g.current_user.follow_topic(topic=topic):
        return topic
    else:
        abort(400)


@api.route('/<topic_id>/reject', methods=['DELETE'])
@jwt_required()
@dump_topic
def reject_invitation(topic_id):
    topic = Topic.get(topic_id)
    g.current_user = current_user
    if g.current_user.reject_invitation(topic):
        return topic
    else:
        abort(400)


@api.route('/<topic_id>/invite/<user_id>', methods=['GET'])
@jwt_required()
@owner_required
@dump_topic
def invite_user_to_topic(topic_id, user_id):
    g.current_user = current_user
    topic = Topic.get(topic_id)
    user = User.get(user_id)
    if g.current_user.invite_user_to_topic(user=user, topic=topic):
        return topic
    abort(400)


@api.route('/<topic_id>/post', methods=['PUT'])
@jwt_required()
@dump_topic
def add_post(topic_id):
    g.current_user = current_user
    topic = Topic.get(topic_id)
    post = post_schema.load(request.get_json())
    if g.current_user.add_post(post, topic):
        return topic
    else:
        abort(400)


"""
CRUD APIs
"""


@api.route('/<topic_id>', methods=['GET'])
@jwt_required()
@dump_topic
def get_by_id(topic_id):
    g.current_user = current_user
    return Topic.get(id=topic_id)


@api.route('/<topic_id>', methods=['PATCH'])
@jwt_required()
@owner_required
@dump_topic
def update_topic(topic_id):
    g.current_user = current_user
    json_raw = request.get_json()
    updated_topic = schema.load(json_raw)
    old_topic = Topic.get(topic_id)
    old_topic.title = updated_topic.title
    result = Topic.update(old_topic)
    if result:
        return old_topic
    else:
        abort(400)


@api.route('/<topic_id>', methods=['DELETE'])
@jwt_required()
@owner_required
def delete_topic(topic_id):
    g.current_user = current_user
    if Topic.delete(topic_id):
        return jsonify({'status': 200, 'message': 'successful'})
    return abort(400)
