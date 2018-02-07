from collections import OrderedDict

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def sql_alchemy_to_json(item: Base):
    d = OrderedDict()
    for column in item.__table__.columns:
        d[column.name] = str(getattr(item, column.name))

    return d


