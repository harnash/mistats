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

        if devices.count() == 0:
            new_device = Device.new_from_device_info(name, info)
            DB.session.add(new_device)

        for dev in devices:
            if dev.token == info.token:
                dev.last_seen = datetime.utcnow()
                DB.session.update(dev)
            else:
                DB.session.delete(dev)

    list_devices()
