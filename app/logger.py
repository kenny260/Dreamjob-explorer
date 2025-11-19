"""
logger.py
Centralized logging setup for DreamJob Explorer.
Provides consistent structured logs across the entire app.
"""

import logging
from .config import DEBUG

# Logging format
LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] "
    "%(name)s: %(message)s"
)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT))

        logger.addHandler(handler)

    return logger

