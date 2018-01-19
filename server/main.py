import time
import os
from prometheus_client import start_http_server, Gauge
from miio.airpurifier import AirPurifier

# Create a metric to track time spent and requests made.
PURIFIER_AQI = Gauge('aqi', 'Air Quality Index')
SERVER_PORT = int(os.getenv('SERVER_PORT', 80))

client = AirPurifier(os.getenv('DEVICE_ADDR'), os.getenv('DEVICE_TOKEN'))


def fetch_aqi():
    status = client.status()
    info = client.info()
    print(info)
    print(status)
    PURIFIER_AQI.set(status.aqi)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(SERVER_PORT)
    # Generate some requests.
    while True:
        fetch_aqi()
        time.sleep(1)
