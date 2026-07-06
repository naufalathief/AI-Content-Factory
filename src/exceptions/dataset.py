"""
Dataset exception module.

This module defines exceptions related to dataset processing.
"""

from __future__ import annotations

from src.exceptions.base import FERFrameworkError


class DatasetError(FERFrameworkError):
    """
    Raised when dataset processing fails.
    """


class DatasetNotFoundError(DatasetError):
    """
    Raised when dataset path or file does not exist.
    """


class InvalidDatasetFormatError(DatasetError):
    """
    Raised when dataset format is invalid.
    """
