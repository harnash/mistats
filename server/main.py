import time
import os

from miio import DeviceException
from prometheus_client import start_http_server, Gauge
from miio.airpurifier import AirPurifier
from common.logging import Logger, initialize_logging
from structlog.processors import format_exc_info

# Create a metric to track time spent and requests made.
from config import SERVER_PORT, LOG_MODE, DEBUG_MODE

DEFAULT_LABELS = ['host', 'model']
PURIFIER_AQI = Gauge('mistats_aqi', 'air quality index', DEFAULT_LABELS)
PURIFIER_AVERAGE_AQI = Gauge('mistats_average_aqi', 'average air quality index', DEFAULT_LABELS)
PURIFIER_HUMIDITY = Gauge('mistats_humidity', 'air humidity', DEFAULT_LABELS)
PURIFIER_POWER = Gauge('mistats_power', 'power state', DEFAULT_LABELS)
PURIFIER_TEMPERATURE = Gauge('mistats_temperature', 'air temperature', DEFAULT_LABELS)
PURIFIER_MOTOR_SPEED = Gauge('mistats_motor_speed', 'fan motor speed', DEFAULT_LABELS)
PURIFIER_LED_BRIGHTNESS = Gauge('mistats_led_brightness', 'led brightness', DEFAULT_LABELS)
PURIFIER_ILLUMINANCE = Gauge('mistats_illuminance', 'level of environment illuminance', DEFAULT_LABELS)
PURIFIER_BUZZER = Gauge('mistats_buzzer', 'is buzzer sound on or off', DEFAULT_LABELS)
PURIFIER_CHILD_LOCK = Gauge('mistats_child_lock', 'is child lock on or off', DEFAULT_LABELS)
PURIFIER_FILTER_LIFE_REMAINING = Gauge('mistats_filter_life_remaining_percentage', 'life span of a filter', DEFAULT_LABELS)
PURIFIER_FILTER_HOURS_USED = Gauge('mistats_filter_used_hours', 'for how many hours filter was in use', DEFAULT_LABELS)
PURIFIER_USE_TIME = Gauge('mistats_use_time_seconds', 'for how many hours device was in use', DEFAULT_LABELS)
PURIFIER_PURIFY_VOLUME = Gauge('mistats_purify_volume_m3', 'how many m3 of air was purified', DEFAULT_LABELS)


logger = Logger('server')


def fetch_aqi(client: 'miio.Device'):
    try:
        status = client.status()
        info = client.info()
    except DeviceException:
        format_exc_info(logger, None, {'exc_info': True})
        return
    except OSError:
        format_exc_info(logger, None, {'exc_info': True})
        return

    labels = [client.ip, info.model]
    logger.debug('status received', **status.data)
    PURIFIER_AQI.labels(*labels).set(status.aqi)
    PURIFIER_AVERAGE_AQI.labels(*labels).set(status.average_aqi)
    PURIFIER_HUMIDITY.labels(*labels).set(status.humidity)
    PURIFIER_POWER.labels(*labels).set(status.is_on)
    PURIFIER_TEMPERATURE.labels(*labels).set(status.temperature)
    PURIFIER_MOTOR_SPEED.labels(*labels).set(status.motor_speed)
    if status.led_brightness is not None:
        PURIFIER_LED_BRIGHTNESS.labels(*labels).set(status.led_brightness.value)
    PURIFIER_ILLUMINANCE.labels(*labels).set(status.illuminance)
    PURIFIER_BUZZER.labels(*labels).set(status.buzzer)
    PURIFIER_CHILD_LOCK.labels(*labels).set(status.child_lock)
    PURIFIER_FILTER_LIFE_REMAINING.labels(*labels).set(status.filter_life_remaining)
    PURIFIER_FILTER_HOURS_USED.labels(*labels).set(status.filter_hours_used)
    PURIFIER_USE_TIME.labels(*labels).set(status.use_time)
    PURIFIER_PURIFY_VOLUME.labels(*labels).set(status.purify_volume)


if __name__ == '__main__':
    initialize_logging(LOG_MODE, DEBUG_MODE)
    # Start up the server to expose the metrics.
    start_http_server(SERVER_PORT)
    # Generate some requests.
    api_client = AirPurifier(os.getenv('DEVICE_ADDR'), os.getenv('DEVICE_TOKEN'))

    while True:
        fetch_aqi(api_client)
        time.sleep(1)
