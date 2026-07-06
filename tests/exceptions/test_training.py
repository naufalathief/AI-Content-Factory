"""
Unit tests for training exceptions.
"""

from src.exceptions.training import (
    CheckpointError,
    TrainingError,
)


def test_training_exception_hierarchy() -> None:
    """
    Training exceptions should inherit TrainingError.
    """

    assert issubclass(
        CheckpointError,
        TrainingError,
    )
