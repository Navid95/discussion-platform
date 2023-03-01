# print(f'-------------------------------------{__name__}----------------------------------------------')

from flask import g, jsonify, request, abort
from main.models import User, Topic, Post
from main.authentication import basic_http
from main.schemas import TopicSchema, PostSchema
from . import topic as api, decorators


auth = basic_http.auth
schema = TopicSchema()
post_schema = PostSchema()
owner_required = basic_http.topic_owner_required
dump_topic = decorators.dump_topic


@api.route('/', methods=['POST'])
@auth.login_required
@dump_topic
def init_topic():
    topic = schema.load(request.get_json())
    if g.current_user.init_topic(topic):
        return topic
    else:
        return jsonify({'message': 'Something wrong happened'})


@api.route('/<topic_id>/follow', methods=['GET'])
@auth.login_required
@dump_topic
def follow_topic(topic_id):
    topic = Topic.get(topic_id)
    if g.current_user.follow_topic(topic=topic):
        return topic
    else:
        abort(400)


@api.route('/<topic_id>/reject', methods=['DELETE'])
@auth.login_required
@dump_topic
def reject_invitation(topic_id):
    topic = Topic.get(topic_id)
    if g.current_user.reject_invitation(topic):
        return topic
    else:
        abort(400)


@api.route('/<topic_id>/invite/<user_id>', methods=['GET'])
@auth.login_required
@owner_required
@dump_topic
def invite_user_to_topic(topic_id, user_id):
    topic = Topic.get(topic_id)
    user = User.get(user_id)
    if g.current_user.invite_user_to_topic(user=user, topic=topic):
        return topic
    abort(400)


@api.route('/<topic_id>/post', methods=['PUT'])
@auth.login_required
@dump_topic
def add_post(topic_id):
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
@auth.login_required
@dump_topic
def get_by_id(topic_id):
    return Topic.get(id=topic_id)


@api.route('/<topic_id>', methods=['PUT', 'PATCH'])
@auth.login_required
@owner_required
@dump_topic
def update_topic(topic_id):
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
@auth.login_required
@owner_required
def delete_topic(topic_id):
    if Topic.delete(topic_id):
        return jsonify({'status': 200, 'message': 'successful'})
    return abort(400)
