import zeroconf
from miio.discovery import Listener
from prometheus_client import start_http_server
from prometheus_client import REGISTRY
from common.logging import Logger, initialize_logging
from stats.collector import MiioDeviceCollector

# Create a metric to track time spent and requests made.
from config import SERVER_PORT, LOG_MODE, DEBUG_MODE, METRIC_PREFIX


logger = Logger('mistats')
listener = Listener()
device_collector = MiioDeviceCollector(listener, METRIC_PREFIX)

if __name__ == '__main__':
    initialize_logging(LOG_MODE, DEBUG_MODE)
    # Start up the server to expose the metrics.
    start_http_server(SERVER_PORT)
    # Generate some requests.
    logger.info('starting service discovery')
    browser = zeroconf.ServiceBrowser(
        zeroconf.Zeroconf(), "_miio._udp.local.", listener)

    REGISTRY.register(device_collector)

    import time

    while True:
        time.sleep(1)
