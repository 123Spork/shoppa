import logging
import re
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from shoppa.core.db import sql_db

log = logging.getLogger(__name__)

camel_2_underscore_re = re.compile('([a-z0-9])([A-Z])')


def camel_2_underscore(class_name):
    """
        A helper function to convert camel-case class names to underscore style names.
    """
    return camel_2_underscore_re.sub(r'\1_\2', class_name).lower()

class SQLDeclarativeMetaClass(DeclarativeMeta):
    def __init__(cls, name, bases, nmspc):
        super(SQLDeclarativeMetaClass, cls).__init__(name, bases, nmspc)
        # register subclasses
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        if hasattr(cls, "__tablename__"):
            cls.registry[cls.__tablename__] = cls
        # remove base classes
        [cls.registry.pop(base) for base in bases if base in cls.registry]


class SQLDeclarativeBase(object):

    def delete(self):
        sql_db.delete(self)

    def save(self):
        sql_db.add(self)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

BaseSQLModel = declarative_base(cls=SQLDeclarativeBase, metaclass=SQLDeclarativeMetaClass)