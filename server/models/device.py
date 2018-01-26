from models import Base
from sqlalchemy import Column, Integer, String


class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    type = Column(String(length=255), nullable=False)
    address = Column(String(length=255), nullable=False)