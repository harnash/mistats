# -*- coding: utf-8 -*-
"""
Borrowed from: https://github.com/stevetarver/ember-falcon-mongo

Logger and LoggerMixin should be the only access to the logging system for
service code.

These classes do several things required by Analytics ELK stack:
    * provide the right flavor of ISO8601 timestamp
    * provide source coordinates: app name, version, hostname
    * remap default log record keys to match existing platform logging conventions
    * censors passwords
    * ensures well-formed json: k-v pairs, newlines escaped, etc.

Note: malformed log records will be dropped during ingestion

The Logger class provides the same interface as the stdlib logging package.
The LoggerMixin class exposes this interface with '_' prefixes to indicate
a protected member.

You can run the logging package in 'local' mode that prints human readable,
colored logs, and 'pd' mode that prints json lines for forwarding to ELK.
To run in local dev mode::

    LOG_MODE=LOCAL ./run_api

FORMATTING:
    Your log message should be the first argument using "".format()::

        self._info('Health server listening at: {}'.format(self._server.url))

    If you use the old method of formatting log messages::

        self._info('Health server listening at: %s', self._server.url)

    the additional parameters will show under key positional_args instead of being
    inserted into the log message. Sometimes these args are just dropped - depending
    on configuration.

    You can add key-value pairs to a log record::

        self._info("Stopping health server...", foo="bar", baz="wombat")

    For exceptions, you can get the exception name with::

        type(exc).__name__

    If you provide the exception as an additional k-v pair named exc_info, a traceback
    will be added to the log record.

    Putting this all together, you can show the exception type, msg, and traceback
    with something like::

        self._error("During shutdown, worker raised {}: {}".format(type(exc).__name__, exc),
                    exc_info=exc)

NOTES:
    * When testing new log entries, ensure that you view log output with and
      without LOG_MODE=LOCAL - they are not perfectly aligned - one may
      cause an error where the other does not.
"""
import datetime
import logging
import logging.config
import platform
import threading
from pythonjsonlogger import jsonlogger

import structlog
from .version import VersionInfo


class LogEntryProcessor:
    """
    Provide log entry processors as well as cached values that are expensive
    to create and thread local storage for request level variables.
    """
    # TODO: need some way to get a pod/node identifier instead of host - or perhaps that will work
    _HOST = platform.node().split('.')[0]
    _VI = VersionInfo()
    _TLS = threading.local()

    @staticmethod
    def add_app_info(_, __, event_dict: dict) -> dict:
        """
        Add application level keys to the event dict
        """
        event_dict['repo_name'] = LogEntryProcessor._VI.repo_name
        event_dict['service_name'] = LogEntryProcessor._VI.service_name
        event_dict['service_version'] = LogEntryProcessor._VI.version
        event_dict['host'] = LogEntryProcessor._HOST
        event_dict['thread_id'] = threading.current_thread().getName()
        return event_dict

    @staticmethod
    def move_event_to_message(_, __, event_dict: dict) -> dict:
        event_dict['message'] = event_dict['event']
        del event_dict['event']
        return event_dict

    @staticmethod
    def add_logger_name(logger, _, event_dict: dict) -> dict:
        """
        Add the logger name to the event dict - using loggerName consistent
        with existing platform logging.
        """
        # TODO: is this still needed - why do we need a loggerName if we include class
        record = event_dict.get("_record")
        if record is None:
            event_dict["loggerName"] = logger.name
        else:
            event_dict["loggerName"] = record.name
        return event_dict


def initialize_logging(mode: str, debug: bool = False) -> None:
    """
    Initialize our logging system:
    * the stdlib logging package for proper structlog use
    * structlog processor chain, etc.

    This should be called once for each application

    NOTES:
    * To enable human readable, colored, positional logging, set LOG_MODE=LOCAL
      Note that this hides many of the boilerplate log entry elements that is
      clutter for local development.
    """

    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    pre_chain = [
        LogEntryProcessor.add_app_info,
        LogEntryProcessor.add_logger_name,
        structlog.stdlib.add_log_level,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if mode.lower() == 'console':
        chain = [
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.dev.ConsoleRenderer(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
        handlers = ['console']
    else:
        chain = pre_chain + [
            LogEntryProcessor.move_event_to_message,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
        handlers = ['json']

    level = 'DEBUG' if debug else 'INFO'

    logging.config.dictConfig({
        "version":                  1,
        "disable_existing_loggers": False,
        "formatters":               {
            "json":   {
                "()":                jsonlogger.JsonFormatter,
            },
            "console": {
                "()":                structlog.stdlib.ProcessorFormatter,
                "processor":         structlog.dev.ConsoleRenderer(colors=True),
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers":                 {
            "console": {
                "level":     level,
                "class":     "logging.StreamHandler",
                "formatter": "console",
            },
            "json":    {
                "level":     level,
                "class":     "logging.StreamHandler",
                "formatter": "json",
            },
        },
        "loggers":                  {
            "": {
                "handlers":  handlers,
                "level":     level,
                "propagate": True,
            },
        }
    })
    structlog.configure(
        processors=chain,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


class LoggerMixin:
    """
    A structured logger that is mixed in to each class

    The mixin methods follow structlog method signatures

    To record an exception in the log: exception type, message, and traceback::

        self._error("During shutdown, worker raised {} exception: {}".format(
                    type(exc).__name__, exc), exc_info=exc)
    """
    @property
    def _logger(self):
        if not getattr(self, '__logger__', None):
            self.__logger__ = structlog.get_logger(type(self).__name__)
        return self.__logger__

    def _debug(self, msg, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, level="Debug", **kwargs)

    def _error(self, msg, *args, **kwargs) -> None:
        self._logger.error(msg, *args, level="Error", **kwargs)

    def _info(self, msg, *args, **kwargs) -> None:
        self._logger.info(msg, *args, level="Info", **kwargs)

    def _warning(self, msg, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, level="Warn", **kwargs)


class Logger(LoggerMixin):
    """
    An instantiable class allowing non-protected access to the LoggerMixin methods.
    Intended for use with functions (things without classes).
    When using this class, you must supply a logger name; by convention, the dotted
    package path.
    """
    def __init__(self, name):
        """
        :param name: required logger name - use dotted package path
        """
        if name is not None and not getattr(self, '__logger__', None):
            self.__logger__ = structlog.get_logger(name)

    def debug(self, msg, *args, **kwargs) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)
