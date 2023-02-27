from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from main.configuration.base import Base

# TODO move to project root

db = SQLAlchemy()
marshmallow = Marshmallow()