"""
Configuration loader module.

This module provides utilities to load experiment configuration
from external YAML files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.constants.datasets import DatasetName
from src.constants.metrics import MetricName
from src.constants.models import (
    BackboneName,
    TransferLearningStrategy,
)
from src.constants.training import OptimizerName
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
                name=DatasetName(
                    data.get(
                        "dataset",
                        {},
                    ).get(
                        "name",
                        DatasetName.FER2013,
                    )
                ),
                image_size=data.get(
                    "dataset",
                    {},
                ).get(
                    "image_size",
                    224,
                ),
                num_classes=data.get(
                    "dataset",
                    {},
                ).get(
                    "num_classes",
                    7,
                ),
            ),
            model=ModelConfig(
                backbone=BackboneName(
                    data.get(
                        "model",
                        {},
                    ).get(
                        "backbone",
                        BackboneName.MOBILENET_V2,
                    )
                ),
                strategy=TransferLearningStrategy(
                    data.get(
                        "model",
                        {},
                    ).get(
                        "strategy",
                        TransferLearningStrategy.FEATURE_EXTRACTION,
                    )
                ),
                pretrained=data.get(
                    "model",
                    {},
                ).get(
                    "pretrained",
                    True,
                ),
            ),
            training=TrainingConfig(
                epochs=data.get(
                    "training",
                    {},
                ).get(
                    "epochs",
                    50,
                ),
                batch_size=data.get(
                    "training",
                    {},
                ).get(
                    "batch_size",
                    32,
                ),
                learning_rate=data.get(
                    "training",
                    {},
                ).get(
                    "learning_rate",
                    0.001,
                ),
                optimizer=OptimizerName(
                    data.get(
                        "training",
                        {},
                    ).get(
                        "optimizer",
                        OptimizerName.ADAM,
                    )
                ),
            ),
            evaluation=EvaluationConfig(
                metrics=tuple(
                    MetricName(metric)
                    for metric in data.get(
                        "evaluation",
                        {},
                    ).get(
                        "metrics",
                        [],
                    )
                )
            ),
        )
