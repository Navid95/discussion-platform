from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_redis import FlaskRedis
from flask_jwt_extended import jwt_manager

db = SQLAlchemy()
marshmallow = Marshmallow()
redis_client = FlaskRedis()
jwt = jwt_manager.JWTManager()