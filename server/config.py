import os

SERVER_PORT = int(os.getenv('SERVER_PORT', 80))
LOG_MODE = os.getenv('LOG_MODE', 'JSON')
DEBUG_MODE = bool(os.getenv('DEBUG', 0))
METRIC_PREFIX = os.getenv('METRIC_PREFIX', 'mistats')
