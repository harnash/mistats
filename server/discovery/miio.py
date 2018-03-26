from typing import Optional

from miio import Device
from miio.discovery import Listener
import zeroconf
from models import Device as DBDevice
from config import DB


class MiioListener(Listener):
    def check_and_create_device(self, info, addr) -> Optional[Device]:
        device_info = super().check_and_create_device(info, addr)

        if device_info is not None:
            dev = DBDevice.new_from_device_info(info.name, device_info)
            dev.enabled = True
            DB.connect()
            
            db_dev = DBDevice.find(DB.session, dev.identifier)
            if db_dev is None:
                DB.session.add(dev)
            elif db_dev.address != dev.address:
                db_dev.address = dev.address

            DB.close()

        return device_info


class MiioServiceDiscovery:
    def __init__(self, listener: MiioListener):
        self.listener = listener
        self.service_browser = zeroconf.ServiceBrowser(zeroconf.Zeroconf(), "_miio._udp.local.", self.listener)
