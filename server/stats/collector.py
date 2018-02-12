from inspect import getmembers
from prometheus_client.core import GaugeMetricFamily
from enum import Enum
from miio.discovery import create_device
from miio.device import DeviceError, DeviceException

from common.logging import Logger
from db import SQLAlchemy
from models import Device


class MiioDeviceCollector(object):
    labels = ['host', 'model', 'identifier']

    def __init__(self, db: SQLAlchemy, prefix: str):
        self.__prefix = prefix
        self.__db = db
        self.__log = Logger('mistats')

    @staticmethod
    def get_class(module, kls):
        m = __import__(module)
        for comp in kls.split('.'):
            m = getattr(m, comp)
        return m

    def collect(self):
        result = []

        self.__db.connect()
        objs = self.__db.session.query(Device).filter(Device.enabled == True).all()
        self.__db.close()

        for device in objs:
            info_class = self.get_class('miio', device.type)
            if info_class is None:
                continue
            ip, _ = device.address.split(':', 1)
            try:
                dev_info = create_device(ip, info_class)
            except DeviceError as e:
                self.__log.error("error connecting to a device", addr=ip, device=info_class,
                                 exc_info=e, stack_info=True)
                continue
            except DeviceException as e:
                self.__log.error("exception connecting to a device", addr=ip, device=info_class,
                                 exc_info=e, stack_info=True)
                continue

            status_method = getattr(dev_info, "status", None)
            label_values = [device.address, device.type, device.identifier]
            if callable(status_method):
                try:
                    status = status_method()
                except DeviceError as e:
                    self.__log.error("error querying device status", addr=ip, device=info_class,
                                     exc_info=e, stack_info=True)
                    continue
                except DeviceException as e:
                    self.__log.error("exception querying device status", addr=ip, device=info_class,
                                     exc_info=e, stack_info=True)
                    continue

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

                    if value.__doc__ is not None:
                        doc = value.__doc__
                    else:
                        doc = ''
                    gauge = GaugeMetricFamily(self.__prefix + '_' + name.lower(), doc, labels=self.labels)

                    gauge.add_metric(label_values, metric_value)
                    result.append(gauge)

        return result
