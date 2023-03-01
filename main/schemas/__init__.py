print(f'-------------------------------------{__name__}----------------------------------------------')

from . import base_schema
BaseSchema = base_schema.BaseSchema

from . import topic_schema
TopicSchema = topic_schema.TopicSchema

from . import post_schema
PostSchema = post_schema.PostSchema

from . import user_schema
UserSchema = user_schema.UserSchema
LoginSchema = user_schema.LoginCredentials
