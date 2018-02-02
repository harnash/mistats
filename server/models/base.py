from collections import OrderedDict

from hug.output_format import json_convert
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


@json_convert(Base)
def device_json(item: Base):
    d = OrderedDict()
    for column in item.__table__.columns:
        d[column.name] = str(getattr(item, column.name))

    return d


