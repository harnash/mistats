import codecs
import time
import hug
from models import Device
from sqlalchemy.orm import Session
from discovery import ServiceDiscovery
from datetime import datetime
from apistar import Route
import typing

from models.base import sql_alchemy_to_json


def list_devices(session: Session) -> typing.List[Device]:
    return [sql_alchemy_to_json(item) for item in session.query(Device).all()]


def activate(session: Session, device_id: int, response: hug.Response):
    item = session.query(Device).filter(Device.id == device_id).first()
    if item is None:
        response.status = HTTP_404
        return "Given id not found"
    item.enabled = True
    return item


def discover():
    if not ServiceDiscovery.service_browser.is_alive():
        ServiceDiscovery.service_browser.start()

        time.sleep(15)

    for name, info in ServiceDiscovery.listener.found_devices.items():
        devices = DB.session.query(Device).filter(Device.address == '{}:{}'.format(info.ip, info.port)).all()

        if len(devices) == 0:
            new_device = Device.new_from_device_info(name, info)
            DB.session.add(new_device)

        for dev in devices:
            new_token = codecs.encode(info.token, 'hex')
            if dev.token == new_token:
                dev.last_seen = datetime.utcnow()
            else:
                DB.session.delete(dev)

    return list_devices()


device_routes = [
    Route('/', 'GET', list_devices)
]