import logging
import sys
import os
from logging.handlers import RotatingFileHandler

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import config

def setup_logging():
    """
    Initialize and configure the application logging system.
    """
    _logger = logging.getLogger(config.APP_NAME)
    _logger.setLevel(config.LOG_LEVEL)
    _logger.propagate = False

    # Clear existing handlers to avoid duplicate logs
    if _logger.handlers:
        for handler in _logger.handlers[:]:
            _logger.removeHandler(handler)

    # Standard Format for Console (Human Readable)
    console_formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    # 1. StreamHandler (Stdout)
    # Use console_formatter for dev, json_formatter for production
    stdout_handler = logging.StreamHandler(sys.stdout)
    if config.ENVIRONMENT == "production":
        # stdout_handler.setFormatter(json_formatter)
        stdout_handler.setFormatter(console_formatter)
    else:
        stdout_handler.setFormatter(console_formatter)

    # 2. RotatingFileHandler
    # Ensure directory exists
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        f"{log_dir}/web_service.log",
        maxBytes=10 * 1024 * 1024, # 10MB
        backupCount=10,
        encoding="utf-8"
    )
    # file_handler.setFormatter(json_formatter)
    file_handler.setFormatter(console_formatter)

    # Add handlers
    _logger.addHandler(stdout_handler)
    _logger.addHandler(file_handler)

    return _logger

# Initialize and export the default logger instance
logger = setup_logging()

async def shutdown_logger():
    """Shudown logger at the end of application lifecycle."""
    logger_obj = logging.getLogger(config.APP_NAME)
    for handler in logger_obj.handlers[:]:
        handler.close()
        logger_obj.removeHandler(handler)

@asynccontextmanager
async def logger_lifespan(app: FastAPI):
    """Lifecycle management for the applicaiton logger."""
    logger.info("*** Starting service: %s", config.SERVICE_NAME)
    app.state.logger = logger
    try:
        yield
    finally:
        logger.info("*** Shutting down service: %s", config.SERVICE_NAME)
        shutdown_logger()

# @TODO use https://pypi.org/project/python-logging-loki-v2/ to push logs to loki

# Initialize and export
# logger = setup_logging()
