print(f'-------------------------------------{__name__}----------------------------------------------')

from . import base, post, topic, user

User = user.User
Topic = topic.Topic
Post = post.Post

# TODO create base class for all models
