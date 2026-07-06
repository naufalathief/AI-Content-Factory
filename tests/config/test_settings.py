"""
Unit tests for global settings configuration.
"""

from dataclasses import FrozenInstanceError

import pytest

from src.config.settings import (
    LoggingSettings,
    ProjectSettings,
    RuntimeSettings,
    Settings,
    settings,
)


def test_settings_instance() -> None:
    """
    Settings singleton should exist.
    """
    assert isinstance(settings, Settings)


def test_project_settings() -> None:
    """
    Project settings should contain valid metadata.
    """
    assert isinstance(settings.project, ProjectSettings)

    assert settings.project.name
    assert settings.project.version


def test_runtime_settings() -> None:
    """
    Runtime settings should contain valid values.
    """
    assert isinstance(settings.runtime, RuntimeSettings)

    assert isinstance(settings.runtime.seed, int)
    assert settings.runtime.device in (
        "auto",
        "cpu",
        "cuda",
    )


def test_logging_settings() -> None:
    """
    Logging settings should contain valid values.
    """
    assert isinstance(settings.logging, LoggingSettings)

    assert settings.logging.level in (
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    )


def test_settings_are_immutable() -> None:
    """
    Settings object should be immutable.
    """
    with pytest.raises(FrozenInstanceError):
        settings.project = ProjectSettings()  # type: ignore[misc]
