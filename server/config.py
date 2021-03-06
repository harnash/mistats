import os
from db import SQLAlchemy


# Declare your config classes with settings variables here
class Config:
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    LOG_MODE = os.getenv('LOG_MODE', 'JSON')
    DEBUG_MODE = bool(os.getenv('DEBUG', 0))
    METRIC_PREFIX = os.getenv('METRIC_PREFIX', 'mistats')


class DevelopmentConfig(Config):
    DEBUG_MODE = bool(os.getenv('DEBUG', 1))


class ProductionConfig(Config):
    pass


ENV_MAPPING = {
    'DEVELOPMENT': DevelopmentConfig,
    'PRODUCTION': ProductionConfig
}

# Globals. If you like move it to separate module
DB = SQLAlchemy(autocommit=True)
CONFIG = ENV_MAPPING[os.environ.get('API_ENV', 'DEVELOPMENT')]