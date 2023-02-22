from main import db
from log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    # TODO add author and date maybe

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    def __str__(self):
        return {'id':self.id,
                'content': self.content,
                'topic_id': self.topic_id}.__str__()





