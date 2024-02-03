from flask_sqlalchemy import SQLAlchemy
import collections
import collections.abc
collections.MutableMapping = collections.abc.MutableMapping

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
