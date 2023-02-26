from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from main.configuration.base import Base

db = SQLAlchemy()
marshmallow = Marshmallow()