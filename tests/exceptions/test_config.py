"""
Unit tests for configuration exceptions.
"""

import pytest

from src.exceptions.base import FERFrameworkError
from src.exceptions.config import ConfigError


def test_config_error() -> None:
    """
    ConfigError should be raised correctly.
    """

    with pytest.raises(ConfigError):
        raise ConfigError(
            "Invalid configuration",
        )


def test_config_error_inheritance() -> None:
    """
    ConfigError should inherit FERFrameworkError.
    """

    assert issubclass(
        ConfigError,
        FERFrameworkError,
    )
