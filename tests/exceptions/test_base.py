"""
Unit tests for base exceptions.
"""

import pytest

from src.exceptions.base import FERFrameworkError


def test_framework_error() -> None:
    """
    Framework error should behave as Exception.
    """

    with pytest.raises(FERFrameworkError):
        raise FERFrameworkError(
            "Test framework error",
        )


def test_framework_error_inheritance() -> None:
    """
    Framework error should inherit from Exception.
    """

    assert issubclass(
        FERFrameworkError,
        Exception,
    )
