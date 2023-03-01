# print(f'-------------------------------------{__name__}----------------------------------------------')

from flask import request, abort, jsonify, g
from main.models import Post
from main.schemas import PostSchema
from main.authentication import basic_http
from .decorators import dump_post
from . import post as api

auth = basic_http.auth
owner_required = basic_http.post_owner_required
schema = PostSchema()


@api.route('/<post_id>', methods=['GET'])
@auth.login_required
@dump_post
def get_by_id(post_id):
    return Post.get(id=post_id)


@api.route('/<post_id>', methods=['PUT', 'PATCH'])
@auth.login_required
@owner_required
@dump_post
def update_post(post_id):
    json_raw = request.get_json()
    updated_topic = schema.load(json_raw)
    old_post = Post.get(post_id)
    old_post.content = updated_topic.content
    result = Post.update(old_post)
    if result:
        return old_post
    else:
        abort(400)


@api.route('/<post_id>', methods=['DELETE'])
@auth.login_required
@owner_required
def delete_post(post_id):
    if Post.delete(post_id):
        return jsonify({'status': 200, 'message': 'successful'})
    return abort(400)
