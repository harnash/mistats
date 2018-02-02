from discovery.miio import MiioServiceDiscovery, MiioListener


def initialize_service_discovery() -> MiioServiceDiscovery:
    global ServiceDiscovery
    ServiceDiscovery = MiioServiceDiscovery(MiioListener())
    return ServiceDiscovery


ServiceDiscovery = initialize_service_discovery()
