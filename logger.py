import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger():
    """Configure and return the AutoHardener logger."""
    logger = logging.getLogger("AutoHardener")

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    log_file = Path(__file__).resolve().parent / "autohardener.log"

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
