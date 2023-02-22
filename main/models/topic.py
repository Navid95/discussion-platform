from main import db
from sqlalchemy.exc import IntegrityError
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

    """
    CRUD methods
    """

    @staticmethod
    def get_instance(id=None, **kwargs):
        if id is not None:
            return Topic.query.filter_by(id=id).first()
        elif kwargs.get('title') is not None:
            return Topic.query.filter_by(title=kwargs['title']).first()
        else:
            return False

    @staticmethod
    def get_all():
        return Topic.query.all()

    @staticmethod
    def delete_instance(id=None, instance=None, **kwargs):
        if id is not None:
            topic = Topic.get_instance(id=id)
        elif instance is not None and isinstance(instance, Topic):
            topic = instance
        elif kwargs.get('title') is not None:
            topic = Topic.get_instance(title=kwargs['title'])
        else:
            return False
        try:
            db.session.delete(topic)
            db.session.commit()
        except BaseException as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def persist(instance):
        try:
            if isinstance(instance, Topic):
                db.session.add(instance)
                db.session.commit()
                return True
            else:
                return False

        except IntegrityError as e:
            logger.warning(e.orig)
            logger.warning(e.orig.args)
            db.session.rollback()
            return False
        except BaseException as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def update(instance):
        pass


