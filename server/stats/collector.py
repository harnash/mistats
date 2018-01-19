from miio.discovery import Listener
from inspect import getmembers
from prometheus_client.core import GaugeMetricFamily
from enum import Enum


class MiioDeviceCollector(object):
    labels = ['host', 'model']

    def __init__(self, listener: Listener, prefix: str):
        self.__listener = listener
        self.__prefix = prefix

    def collect(self):
        result = []

        for addr, device in self.__listener.found_devices.items():
            status_method = getattr(device, "status", None)
            info = device.info()
            label_values = [addr, info.model]
            if callable(status_method):
                status = status_method()

                for name, value in getmembers(status.__class__):
                    if not isinstance(value, property):
                        continue

                    metric_value = getattr(status, name)
                    if metric_value is None:
                        continue

                    if isinstance(metric_value, Enum):
                        metric_value = metric_value.value

                    try:
                        metric_value = float(metric_value)
                    except ValueError:
                        continue

                    gauge = GaugeMetricFamily(self.__prefix + '_' + name.lower(), value.__doc__, labels=self.labels)

                    gauge.add_metric(label_values, metric_value)
                    result.append(gauge)

        return result
