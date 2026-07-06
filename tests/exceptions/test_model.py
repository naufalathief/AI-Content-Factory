"""
Unit tests for model exceptions.
"""

from src.exceptions.model import (
    ModelError,
    UnsupportedModelError,
)


def test_model_exception_hierarchy() -> None:
    """
    Model exceptions should inherit ModelError.
    """

    assert issubclass(
        UnsupportedModelError,
        ModelError,
    )
