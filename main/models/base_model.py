from ..extensions import db
from datetime import datetime


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
        pass

    @staticmethod
    def save(instance):
        pass

    @staticmethod
    def update(instance):
        pass

    @staticmethod
    def delete(id):
        pass
