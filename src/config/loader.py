"""
Configuration loader module.

This module provides utilities to load experiment configuration
from external YAML files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.config.experiment import (
    DatasetConfig,
    EvaluationConfig,
    ExperimentConfig,
    ModelConfig,
    TrainingConfig,
)


def load_experiment_config(config_path: Path) -> ExperimentConfig:
    """
    Load experiment configuration from YAML file.

    Args:
        config_path: Path to YAML configuration file.

    Returns:
        Parsed experiment configuration.

    Raises:
        FileNotFoundError:
            If configuration file does not exist.
    """

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        data: dict[str, Any] = yaml.safe_load(file)

    return ExperimentConfig(
        dataset=DatasetConfig(
            **data.get("dataset", {}),
        ),
        model=ModelConfig(
            **data.get("model", {}),
        ),
        training=TrainingConfig(
            **data.get("training", {}),
        ),
        evaluation=EvaluationConfig(
            **data.get("evaluation", {}),
        ),
    )
