# common_logging/logging_config.py
import os
import logging.config
from pathlib import Path

from dotenv import load_dotenv


# Module level flag to indicate if the logging has been configured
LOGGING_CONFIGURED = False
CWD = Path.cwd().parent.resolve()

def _load_env():
    # look for the one .env in your repo root (cwd or above)
    for p in (CWD, *CWD.parents):
        f = p / ".env"
        if f.is_file():
            load_dotenv(str(f), override=False)
            return

def configure_logging():
    """
    Configures the logging system for the application.
    This function sets up the logging configuration based on environment variables
    and ensures that the logging system is only configured once.
    """
    global LOGGING_CONFIGURED
    if LOGGING_CONFIGURED:
        return
    LOGGING_CONFIGURED = True
        
    # Load environment variables from .env file
    _load_env()
    
    # Extract env variable for log level, default to INFO if not set
    lvl = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Set the logging configuration
    cfg = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(name)s [%(levelname)s] %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": lvl,
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": str(Path.cwd() / "gem_screening.log"),
                "maxBytes": 10*1024*1024,
                "backupCount": 5,
                "encoding": "utf8",
                "level": lvl,
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": lvl,
        },
    }
    
    # Configure the logging system
    logging.config.dictConfig(cfg)
