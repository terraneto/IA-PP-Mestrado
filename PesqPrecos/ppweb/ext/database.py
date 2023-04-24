from flask_sqlalchemy import SQLAlchemy
import collections.abc
import collections
collections.MutableMapping = collections.abc.MutableMapping

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
