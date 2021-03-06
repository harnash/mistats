import codecs
from datetime import datetime
import miio.discovery
from typing import Optional

from models import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.orm import Session


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer(), primary_key=True)
    type = Column(String(length=255), nullable=False)
    address = Column(String(length=255), nullable=False)
    identifier = Column(String(length=255), nullable=False, unique=True)
    token = Column(String(length=255), nullable=False)
    enabled = Column(Boolean(), default=True)
    last_seen = Column(TIMESTAMP(), nullable=False, default=datetime.utcnow)
    updated = Column(TIMESTAMP(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    added = Column(TIMESTAMP(), nullable=False, default=datetime.utcnow)

    @staticmethod
    def check_if_exists(db: Session, item: 'Device') -> bool:
        return db.query(Device).filter(Device.identifier == item.identifier).scalar() is not None

    @staticmethod
    def find(db: Session, identifier: str) -> Optional['Device']:
        return db.query(Device).filter(Device.identifier == identifier).scalar()

    @staticmethod
    def new_from_device_info(identifier: str, device_info: miio.discovery.Device) -> 'Device':
        return Device(
            type=device_info.__class__.__name__,
            address='{}:{}'.format(device_info.ip, device_info.port),
            identifier=identifier,
            token=codecs.encode(device_info.token, 'hex')
        )
