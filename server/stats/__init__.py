from stats.collector import MiioDeviceCollector

DeviceCollector = None


def initialize_collector(db: 'db.SQLAlchemy', metrics_prefix: str) -> MiioDeviceCollector:
    global DeviceCollector
    DeviceCollector = MiioDeviceCollector(db, metrics_prefix)
    return DeviceCollector
