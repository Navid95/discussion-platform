from main import db
from log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)


class Topic(db.Model):
    __tablename__ = 'topic'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('Post', backref='topic', lazy='dynamic')

    def __repr__(self):
        return {'id': self.id,
                'title': self.title,
                'owner_id': self.owner_id
                }.__str__()

