import logging
import sys
from logging.config import dictConfig


def setup_logging():
    """
    Configure structured JSON logging for the application.
    """

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "format": (
                        '{"timestamp": "%(asctime)s", '
                        '"level": "%(levelname)s", '
                        '"logger": "%(name)s", '
                        '"message": "%(message)s"}'
                    ),
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "stream": sys.stdout,
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["default"],
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    """
    return logging.getLogger(name)