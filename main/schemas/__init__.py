print(f'-------------------------------------{__name__}----------------------------------------------')

from . import user_schema, topic_schema, post_schema

UserSchema = user_schema.UserSchema
TopicSchema = topic_schema.TopicSchema
PostSchema = post_schema.PostSchema

