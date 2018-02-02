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
            DB.connect()
            DB.session.add(dev)
            DB.close()

        return device_info


class MiioServiceDiscovery:
    def __init__(self, listener: MiioListener):
        self.listener = listener
        self.service_browser = zeroconf.ServiceBrowser(zeroconf.Zeroconf(), "_miio._udp.local.", self.listener)
