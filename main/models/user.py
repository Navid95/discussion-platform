from main import db
from sqlalchemy.exc import IntegrityError
from log_utils import init_logger
from werkzeug.security import generate_password_hash
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(100), nullable=False)

    topics = db.relationship('Topic', backref='owner', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return {'id': self.id,
                'email': self.email,
                'password_hash': self.password_hash
                # 'topics': self.topics
                }.__str__()

    # TODO read more about python @property and decorators
    @property
    def password(self):
        logger.warning(f'attempted to read {User} instance {self} password!')
        raise AttributeError('password field not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    """
    CRUD methods
    """

    @staticmethod
    def get_instance(id=None, **kwargs):
        if id is not None:
            return User.query.filter_by(id=id).first()
        elif kwargs.get('email') is not None:
            return User.query.filter_by(email=kwargs['email']).first()
        else:
            return False

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def delete_instance(id=None, instance=None, **kwargs):
        if id is not None:
            user = User.get_instance(id=id)
        elif instance is not None and isinstance(instance, User):
            user = instance
        elif kwargs.get('email') is not None:
            user = User.get_instance(email=kwargs['email'])
        else:
            return False
        try:
            db.session.delete(user)
            db.session.commit()
        except BaseException as e:
            logger.exception(e)
            db.session.rollback()
            return False

    @staticmethod
    def persist(instance):
        try:
            if isinstance(instance, User):
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

    # TODO check why simple python assignment on a field (exp. email) changes the db row (test_models.test_user_crud Update section)
    @staticmethod
    def update(instance):
        pass


