"""
Unit tests for logger utilities.
"""

import logging

from src.utils.logger import get_logger


def test_get_logger() -> None:
    """
    Logger should be created.
    """

    logger = get_logger(
        "test_logger",
    )

    assert isinstance(
        logger,
        logging.Logger,
    )


def test_logger_level() -> None:
    """
    Logger level should be configurable.
    """

    logger = get_logger(
        "debug_logger",
        logging.DEBUG,
    )

    assert logger.level == logging.DEBUG
