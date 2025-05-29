# common_logging/logging_config.py
import os
import logging.config
from pathlib import Path

from dotenv import load_dotenv


def _load_env():
    # look for the one .env in your repo root (cwd or above)
    here = Path.cwd().resolve()
    for p in (here, *here.parents):
        f = p / ".env"
        if f.is_file():
            load_dotenv(str(f), override=False)
            return

def configure():
    _load_env()
    lvl = os.getenv("LOG_LEVEL", "INFO").upper()
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
    logging.config.dictConfig(cfg)
