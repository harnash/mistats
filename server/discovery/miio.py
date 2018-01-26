from miio.discovery import Listener
import zeroconf


class MiioServiceDiscovery:
    def __init__(self, listener: Listener):
        self.listener = listener
        self.service_browser = zeroconf.ServiceBrowser(zeroconf.Zeroconf(), "_miio._udp.local.", self.listener)
