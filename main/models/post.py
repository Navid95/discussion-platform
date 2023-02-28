print(f'-------------------------------------{__name__}----------------------------------------------')

from extensions import db
from sqlalchemy.exc import IntegrityError
from main.models.base_model import BaseModel
from main.utilities import app_logger as logger


class Post(BaseModel):
    __tablename__ = 'post'
    # id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return {'id': self.id,
                'content': self.content,
                'topic_id': self.topic_id,
                'author_id': self.author_id}.__str__()

    """
    CRUD methods
    """

    @staticmethod
    def get_instance(id=None, **kwargs):
        if id is not None:
            return Post.query.filter_by(id=id).first()
        else:
            return False

    @staticmethod
    def get_all():
        return Post.query.all()

    @staticmethod
    def delete_instance(id=None, instance=None, **kwargs):
        if id is not None:
            logger.debug(f'got id {id} to delete')
            post = Post.get_instance(id=id)
        elif instance is not None and isinstance(instance, Post):
            logger.debug(f'got {instance} to delete')
            post = instance
        else:
            return False
        try:
            db.session.delete(post)
            db.session.commit()
        except BaseException as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def persist(instance):
        try:
            if isinstance(instance, Post):
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
            if isinstance(instance, Post):
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
        return Post.query.filter_by(id=id).first()

    def update(instance):
        return Post.save(instance)

    def delete(id):
        try:
            db.session.delete(Post.get(id=id))
            db.session.commit()
            return True
        except BaseException as e:
            logger.exception(f'exception in deleting User with id={id}. Trying to rollback')
            db.session.rollback()
            return False


"""
marshmallow schema
"""

# class PostSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = Post
#         include_fk = True
#
#     id = ma.auto_field()
#     content = ma.auto_field()
#     topic_id = ma.auto_field()
#     author_id = ma.auto_field()
