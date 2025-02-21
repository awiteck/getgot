import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
import os

from getgot.settings import settings

def setup_file_handler(log_dir: str = "logs") -> RotatingFileHandler:
    """
    Setup and return a rotating file handler.
    File handler writes to disk
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Setup rotating file handler
    log_file = os.path.join(log_dir, "app.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    )
    
    return file_handler

def setup_stream_handler() -> logging.StreamHandler:
    """
    Setup and return a stream handler for console output.
    Stream handler writes to console
    """
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    )
    return stream_handler

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: The name for the logger. If None, returns the root logger.
    
    Returns:
        A configured logger instance.
    
    Usage:
        logger = get_logger(__name__)
        logger.info("This is an info message")
        logger.error("This is an error message")
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        log_level = settings.LOG_LEVEL.upper()
        logger.setLevel(getattr(logging, log_level))

        logger.addHandler(setup_stream_handler())
        logger.addHandler(setup_file_handler())

        logger.propagate = False

    return logger