from functools import wraps
from main.schemas import TopicSchema

schema = TopicSchema()


def dump_topic(f):

    @wraps(f)
    def to_json(*args, **kwargs):
        value = f(*args, **kwargs)
        return schema.dumps(value)
    return to_json
