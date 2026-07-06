"""
Logging utility.

This module provides centralized logger creation
for experiment tracking.
"""

from __future__ import annotations

import logging


def get_logger(
    name: str,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Create configured logger instance.

    Args:
        name: Logger name.
        level: Logging level.

    Returns:
        Configured logger.
    """

    logger = logging.getLogger(name)

    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
