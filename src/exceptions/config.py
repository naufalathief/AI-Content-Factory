"""
Configuration exception module.

This module defines exceptions related to configuration errors.
"""

from __future__ import annotations

from src.exceptions.base import FERFrameworkError


class ConfigError(FERFrameworkError):
    """
    Raised when configuration processing fails.
    """
