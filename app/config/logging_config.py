"""Central logging configuration for the calculator app.

Provides a single function, :func:`configure_logging`, that applies a
stream-based handler and a consistent formatter to the ``calculator``
logger. Importing this module will configure logging once. The function
is idempotent and safe to call multiple times.
"""
import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    root_logger = logging.getLogger("calculator")
    if root_logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


# Configure at import time so modules importing calculator get logging configured
configure_logging()
