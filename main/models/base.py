print(f'-------------------------------------{__name__}----------------------------------------------')

from datetime import datetime
from ..extensions import db
from log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)

print(f'-------------------------------{__name__}-----------------------------------')


class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_updated_at = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.Integer, nullable=False)

    def __init__(self):
        self.created_at = datetime.utcnow()
        self.last_updated_at = self.created_at
        self.version = 0

    @staticmethod
    def save(instance):
        pass

    @staticmethod
    def get(id):
        return __class__.query.filter_by(id=id).first()


    @staticmethod
    def delete(id):
        pass

    @staticmethod
    def update(id):
        pass


