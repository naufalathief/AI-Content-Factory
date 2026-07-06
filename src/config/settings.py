"""
Global settings configuration module.

This module defines application-level settings for the
FER Transfer Learning Framework.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectSettings:
    """
    Project metadata settings.

    Attributes:
        name: Project name.
        version: Project version.
        description: Project description.
    """

    name: str = "FER Transfer Learning Framework"
    version: str = "0.1.0"
    description: str = (
        "Facial Expression Recognition Transfer Learning Research Framework"
    )


@dataclass(frozen=True, slots=True)
class RuntimeSettings:
    """
    Runtime execution settings.

    Attributes:
        seed: Random seed value.
        device: Computation device.
        deterministic: Enable deterministic execution.
    """

    seed: int = 42
    device: str = "auto"
    deterministic: bool = True


@dataclass(frozen=True, slots=True)
class LoggingSettings:
    """
    Logging configuration settings.

    Attributes:
        level: Logging level.
        format: Logging message format.
    """

    level: str = "INFO"
    format: str = "%(asctime)s - %(levelname)s - %(message)s"


@dataclass(frozen=True, slots=True)
class Settings:
    """
    Global framework settings container.

    Attributes:
        project: Project settings.
        runtime: Runtime settings.
        logging: Logging settings.
    """

    project: ProjectSettings = ProjectSettings()
    runtime: RuntimeSettings = RuntimeSettings()
    logging: LoggingSettings = LoggingSettings()


settings = Settings()
