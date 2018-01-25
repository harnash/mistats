import zeroconf
import hug
from miio.discovery import Listener
from prometheus_client import REGISTRY
from prometheus_client.exposition import generate_latest

from common.logging import initialize_logging
from middleware.accesslog import AccessLogMiddleware
from stats.collector import MiioDeviceCollector

# Create a metric to track time spent and requests made.
from config import db, config

app = hug.API(__name__)

# init DB
db.init_app(app, config.SQLALCHEMY_DATABASE_URI)


service_browser = None


@hug.startup()
def init(api: hug.API):
    global service_browser
    initialize_logging(config.LOG_MODE, debug=config.DEBUG_MODE)
    listener = Listener()
    device_collector = MiioDeviceCollector(listener, config.METRIC_PREFIX)
    service_browser = zeroconf.ServiceBrowser(
        zeroconf.Zeroconf(), "_miio._udp.local.", listener)

    REGISTRY.register(device_collector)
    api.http.add_middleware(AccessLogMiddleware())


@hug.get(output=hug.output_format.text)
def stats():
    return generate_latest(REGISTRY).decode('utf8')
