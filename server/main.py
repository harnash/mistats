import zeroconf
import hug
from miio.discovery import Listener
from prometheus_client import REGISTRY

from common.logging import initialize_logging, Logger
from middleware.accesslog import setup_access_log
from stats.collector import MiioDeviceCollector

from config import DB, CONFIG
import routers


service_browser = None
app = hug.API(__name__)

router = hug.route.API(app)
router.get('/stats', output=hug.output_format.text, api=app)(routers.generate_stats)

router.get('/device', api=app)(routers.list_devices)

initialize_logging(CONFIG.LOG_MODE, debug=CONFIG.DEBUG_MODE)
setup_access_log(app, Logger('access_log'))
DB.init_app(app, CONFIG.SQLALCHEMY_DATABASE_URI)
DB.create_models()


@hug.exception(api=app)
def handle_exception(exception):
    log = Logger('mistats')
    log.error("exception occurred", exc_info=exception, stack_info=True)
    raise hug.HTTPInternalServerError('Something broke', 'Something broke')


@hug.startup(api=app)
def init(api: hug.API):
    global service_browser
    listener = Listener()
    device_collector = MiioDeviceCollector(listener, CONFIG.METRIC_PREFIX)
    service_browser = zeroconf.ServiceBrowser(
        zeroconf.Zeroconf(), "_miio._udp.local.", listener)

    REGISTRY.register(device_collector)
