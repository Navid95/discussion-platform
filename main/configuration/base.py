from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table
from datetime import datetime


class Base(Model):
    # __abstract__ = True

    @declared_attr
    def id(cls):
        id = sa.Column(sa.Integer, primary_key=True)
        return id

    @declared_attr
    def created(cls):
        created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow())
        return created

    @declared_attr
    def updated(cls):
        updated = sa.Column(sa.DateTime, onupdate=datetime.utcnow())
        return updated


    # @staticmethod
    # def save(instance):
    #
    #     pass
    #
    # @staticmethod
    # def get(id: int):
    #     return Base.query.filter_by(id=id)
    #
    # @staticmethod
    # def delete(id):
    #     pass
    #
    # @staticmethod
    # def update(id):
    #     pass


