import time

import zeroconf
from miio import DeviceException, AirPurifier
from miio.discovery import Listener
from prometheus_client import start_http_server
from common.logging import Logger, initialize_logging
from structlog.processors import format_exc_info
import stats.air_purifier

# Create a metric to track time spent and requests made.
from config import SERVER_PORT, LOG_MODE, DEBUG_MODE


logger = Logger('mistats')
listener = Listener()


def fetch_aqi(addr: str, device: 'miio.Device'):
    logger.debug("polling device", ip=addr)
    try:
        info = device.info()
    except DeviceException:
        format_exc_info(logger, None, {'exc_info': True})
        return
    except OSError:
        format_exc_info(logger, None, {'exc_info': True})
        return

    labels = [addr, info.model]

    if isinstance(device, AirPurifier):
        status = device.status()
        logger.debug('status received', **status.data)
        stats.air_purifier.process(status, labels)
    else:
        logger.debug('unsupported device', ip=addr)


if __name__ == '__main__':
    initialize_logging(LOG_MODE, DEBUG_MODE)
    # Start up the server to expose the metrics.
    start_http_server(SERVER_PORT)
    # Generate some requests.
    logger.info('starting service discovery')
    browser = zeroconf.ServiceBrowser(
        zeroconf.Zeroconf(), "_miio._udp.local.", listener)

    while True:
        for addres, device in listener.found_devices.items():
            fetch_aqi(addres, device)
        time.sleep(1)
