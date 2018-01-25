import os

LOG_MODE = os.getenv('LOG_MODE', 'JSON')
DEBUG_MODE = bool(os.getenv('DEBUG', 0))
METRIC_PREFIX = os.getenv('METRIC_PREFIX', 'mistats')
