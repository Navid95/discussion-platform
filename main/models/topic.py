print(f'-------------------------------------{__name__}----------------------------------------------')

from extensions import db
from sqlalchemy.exc import IntegrityError
from .base_model import BaseModel
from main.utilities import app_logger as logger


class Topic(BaseModel):
    __tablename__ = 'topic'

    # id = db.Column(db.Integer, primary_key=True)
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
    def update_instance(instance):
        pass

    """
    Inherited CRUD methods
    """

    def save(instance):
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

    def get(id):
        return Topic.query.filter_by(id=id).first()

    def update(instance):
        return Topic.save(instance)

    def delete(id):
        try:
            db.session.delete(Topic.get(id=id))
            db.session.commit()
            return True
        except BaseException as e:
            logger.exception(f'exception in deleting User with id={id}. Trying to rollback')
            db.session.rollback()
            return False

    """
    business logic
    """

    def add_post(self, post):
        self.posts.append(post)
        db.session.add(self)
        db.session.commit()


"""
marshmallow schema
"""

# class TopicSchema(ma.SQLAlchemySchema):
#     # from .post import PostSchema
#     # from .user import UserSchema
#
#     class Meta:
#         model = Topic
#         include_fk = True
#
#     id = ma.auto_field()
#     title = ma.auto_field()
#     owner_id = ma.auto_field()
#     posts = ma.Nested(model.PostSchema, many=True)
