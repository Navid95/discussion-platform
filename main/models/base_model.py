from extensions import db
from datetime import datetime
from main.utilities import app_logger as logger


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

    """
    CRUD methods
    """

    @staticmethod
    def get(id):
        return BaseModel.query.filter_by(id=id).first()

    @staticmethod
    def save(instance):
        pass

    @staticmethod
    def update(instance):
        pass

    @staticmethod
    def delete(id):
        pass
