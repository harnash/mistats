from models import Device
from config import DB


def list_devices():
    db = DB
    return db.session.query(Device).all()
