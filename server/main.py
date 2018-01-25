import logging

import zeroconf
import hug
from miio.discovery import Listener
from prometheus_client import REGISTRY
from prometheus_client.exposition import generate_latest
from common.logging import initialize_logging, Logger
from stats.collector import MiioDeviceCollector

# Create a metric to track time spent and requests made.
from config import SERVER_PORT, LOG_MODE, DEBUG_MODE, METRIC_PREFIX


service_browser = None


@hug.startup()
def init(api):
    global service_browser
    initialize_logging(LOG_MODE)
    listener = Listener()
    device_collector = MiioDeviceCollector(listener, METRIC_PREFIX)
    service_browser = zeroconf.ServiceBrowser(
        zeroconf.Zeroconf(), "_miio._udp.local.", listener)

    REGISTRY.register(device_collector)


@hug.get(output=hug.output_format.text)
def stats():
    logger = logging.getLogger("stats")
    logger.info('getting stats')
    l = Logger("foo")
    l.info("foo", bar='df')
    return generate_latest(REGISTRY).decode('utf8')
