from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_redis import FlaskRedis

db = SQLAlchemy()
marshmallow = Marshmallow()
redis_client = FlaskRedis()
