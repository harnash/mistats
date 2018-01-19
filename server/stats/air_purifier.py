from typing import List

from prometheus_client import Gauge

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


def process(status: 'miio.AirPurifierStatus', labels: List[str]):
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
