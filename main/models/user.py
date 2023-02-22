from main import db
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
