"""
Training exception module.

This module defines exceptions related to training execution.
"""

from __future__ import annotations

from src.exceptions.base import FERFrameworkError


class TrainingError(FERFrameworkError):
    """
    Raised when training process fails.
    """


class CheckpointError(TrainingError):
    """
    Raised when checkpoint operation fails.
    """
