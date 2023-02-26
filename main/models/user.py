print(f'-------------------------------------{__name__}----------------------------------------------')

from ..extensions import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from log_utils import init_logger
import logging

init_logger(__name__)
logger = logging.getLogger(__name__)
print(f'-------------------------------{__name__}-----------------------------------')

# TODO all custom configs should be created at app initialization in json format

TOKEN_EXP_KEY = 'exp'
TOKEN_SENDER_KEY = 'sender'
TOKEN_RECEIVER_KEY = 'receiver'
TOKEN_TOPIC_KEY = 'topic_id'

user_follows = db.Table('user_follows',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True))

user_waiting_acceptance=db.Table('user_waiting',
                                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                                 db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True))


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(100), nullable=False)

    topics = db.relationship('Topic', backref='owner', lazy='dynamic',collection_class=list)
    follows = db.relationship('Topic', secondary=user_follows, backref='followers')
    waiting_accept=db.relationship('Topic', secondary=user_waiting_acceptance, backref='invites')
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return {'id': self.id,
                'email': self.email,
                'password_hash': self.password_hash,
                'topics': self.topics
                }.__str__()

    # TODO read more about python @property and decorators
    @property
    def password(self):
        logger.warning(f'attempted to read {User} instance {self} password!')
        raise AttributeError('password field not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    """
    CRUD methods
    """
# TODO CRUD methods should only work with <id>, others should be defined in separate methods/apis
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

    """
    business logic
    """

    def follow_topic(self, topic):
        if not self.has_followed(topic):
            self.follows.append(topic)
            db.session.add(self)
            db.session.commit()
        else:
            return False

    def init_topic(self, topic):
        self.topics.append(topic)
        self.follow_topic(topic=topic)
        db.session.add(self)
        db.session.commit()

    def has_followed(self, topic):
        return topic in self.follows

    def owns_topic(self, topic):
        return topic in self.topics

    def is_in_waiting_list(self, topic):
        return topic in self.waiting_accept

    def invite_user_to_topic(self, user, topic):
        if self.owns_topic(topic) and not user.has_followed(topic) and not user.is_in_waiting_list(topic):
            user.waiting_accept.append(topic)
            db.session.add(user)
            db.session.commit()
        else:
            return False


"""
functions
"""

# def encode_token(raw_token, expiration=3600):
#     # import discussion
#     # app = discussion.app
#     raw_token[TOKEN_EXP_KEY] = datetime.now() + timedelta(seconds=expiration)
#     return jwt.encode(payload=raw_token, key='discussion app secret key',
#                       algorithm='HS256')
#
#
# def decode_token(token):
#     import discussion
#     app = discussion.app
#     return jwt.decode(jwt=token, key='discussion app secret key',
#                       algorithms='HS256')
