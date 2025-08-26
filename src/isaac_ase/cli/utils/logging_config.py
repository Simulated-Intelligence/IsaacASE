from __future__ import annotations

import logging
import sys
from logging import handlers
from pathlib import Path

try:
    # Provides ANSI coloured output
    from colorlog import ColoredFormatter
except ModuleNotFoundError:  # Graceful degradation when colour library absent
    ColoredFormatter = None


def setup_logging(
    *,
    log_dir: str | Path = "logs",
    log_file: str = "app.log",
    level: int | str = logging.INFO,
    rotation: str = "midnight",
    retention: int = 7,
) -> None:
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    file_path = log_dir / log_file

    root = logging.getLogger()
    root.setLevel(level)

    root.handlers.clear()

    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if ColoredFormatter is not None and sys.stderr.isatty():
        console_formatter: logging.Formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    else:
        console_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )

    file_handler = handlers.TimedRotatingFileHandler(
        file_path,
        when=rotation,
        backupCount=retention,
        encoding="utf-8",
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    root.addHandler(file_handler)
    root.addHandler(console_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)