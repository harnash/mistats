from discovery.miio import MiioServiceDiscovery, Listener


def initialize_service_discovery() -> MiioServiceDiscovery:
    global ServiceDiscovery
    ServiceDiscovery = MiioServiceDiscovery(Listener())
    return ServiceDiscovery


ServiceDiscovery = initialize_service_discovery()
