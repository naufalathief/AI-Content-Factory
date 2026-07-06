"""
Base exception module.

This module defines the root exception class for the
FER Transfer Learning Framework.
"""

from __future__ import annotations


class FERFrameworkError(Exception):
    """
    Base exception for all framework errors.

    All custom framework exceptions should inherit
    from this class.
    """
