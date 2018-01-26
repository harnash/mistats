from datetime import datetime

from models import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer(), primary_key=True)
    type = Column(String(length=255), nullable=False)
    address = Column(String(length=255), nullable=False)
    enabled = Column(Boolean(), default=True)
    last_seen = Column(TIMESTAMP(), nullable=False, default=datetime.utcnow)
    updated = Column(TIMESTAMP(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    added = Column(TIMESTAMP(), nullable=False, default=datetime.utcnow)
