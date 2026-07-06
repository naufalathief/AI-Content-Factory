"""
Model exception module.

This module defines exceptions related to model processing.
"""

from __future__ import annotations

from src.exceptions.base import FERFrameworkError


class ModelError(FERFrameworkError):
    """
    Raised when model processing fails.
    """


class UnsupportedModelError(ModelError):
    """
    Raised when requested model architecture is unsupported.
    """
