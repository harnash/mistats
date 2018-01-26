import signal
import sys
import hug
from prometheus_client import REGISTRY

from common.logging import initialize_logging, Logger
from middleware.accesslog import setup_access_log
from stats import initialize_collector
from discovery import ServiceDiscovery

from config import DB, CONFIG
import routers


app = hug.API(__name__)

router = hug.route.API(app)
router.get('/stats', output=hug.output_format.text, api=app)(routers.generate_stats)

router.get('/devices', api=app)(routers.list_devices)
router.post('/devices/discover', api=app)(routers.do_discovery)

initialize_logging(CONFIG.LOG_MODE, debug=CONFIG.DEBUG_MODE)
setup_access_log(app, Logger('access_log'))
DB.init_app(app, CONFIG.SQLALCHEMY_DATABASE_URI)
DB.create_models()


def signal_handler(signal, frame):
    if ServiceDiscovery.service_browser.is_alive():
        ServiceDiscovery.service_browser.cancel()

    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


@hug.exception(api=app)
def handle_exception(exception):
    log = Logger('mistats')
    log.error("exception occurred", exc_info=exception, stack_info=True)
    raise hug.HTTPInternalServerError('Something broke', 'Something broke')


@hug.startup(api=app)
def init(_):
    REGISTRY.register(initialize_collector(ServiceDiscovery.listener, CONFIG.METRIC_PREFIX))
