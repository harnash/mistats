import time
import os
from prometheus_client import start_http_server, Gauge
from miio.airpurifier import AirPurifier
from common.logging import Logger, initialize_logging

# Create a metric to track time spent and requests made.
from config import SERVER_PORT, LOG_MODE, DEBUG_MODE

PURIFIER_AQI = Gauge('aqi', 'Air Quality Index')

logger = Logger('server')

def fetch_aqi(client: 'miio.Device'):
    status = client.status()
    logger.debug('status received', **status.data)
    PURIFIER_AQI.set(status.aqi)


if __name__ == '__main__':
    initialize_logging(LOG_MODE, DEBUG_MODE)
    # Start up the server to expose the metrics.
    start_http_server(SERVER_PORT)
    # Generate some requests.
    api_client = AirPurifier(os.getenv('DEVICE_ADDR'), os.getenv('DEVICE_TOKEN'))

    while True:
        fetch_aqi(api_client)
        time.sleep(1)
