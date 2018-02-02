import codecs
import time
from models import Device
from config import DB
from discovery import ServiceDiscovery
from datetime import datetime


def list_devices():
    return DB.session.query(Device).all()


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
