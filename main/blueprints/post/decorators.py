from functools import wraps
from main.schemas import PostSchema

schema = PostSchema()


def dump_post(f):

    @wraps(f)
    def to_json(*args, **kwargs):
        value = f(*args, **kwargs)
        return schema.dumps(value)
    return to_json
