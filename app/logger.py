"""
Logger Configuration for the Application.

This module configures the logging system for the application. It uses `pythonjsonlogger`
to format logs in JSON format and attaches a stream handler for outputting logs. The logger
is configured based on the application settings, and the timestamp is added to each log entry.

Attributes:
    logger (Logger): The configured logger instance for the application.
    logHandler (StreamHandler): The stream handler that outputs logs.
    formatter (CustomJsonFormatter): The custom formatter that outputs logs in JSON format.
"""

import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from config import settings

logger = logging.getLogger()
logHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Custom formatter for logging that adds a timestamp and normalizes the log level.

    This formatter formats the log record as JSON, adding fields such as the timestamp
    and the log level. It ensures logs are structured and consistent across the application.
    """

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)
