from stats.collector import MiioDeviceCollector

DeviceCollector = None


def initialize_collector(listener: 'miio.discovery.Listener', metrics_prefix: str) -> MiioDeviceCollector:
    global DeviceCollector
    DeviceCollector = MiioDeviceCollector(listener, metrics_prefix)
    return DeviceCollector
