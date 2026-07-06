"""
Experiment configuration module.

This module defines experiment-level configuration used for
training and evaluating transfer learning strategies.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.constants.datasets import DatasetName
from src.constants.metrics import MetricName
from src.constants.models import (
    BackboneName,
    TransferLearningStrategy,
)
from src.constants.training import OptimizerName


@dataclass(frozen=True, slots=True)
class DatasetConfig:
    """
    Dataset configuration.
    """

    name: DatasetName = DatasetName.FER2013
    image_size: int = 224
    num_classes: int = 7


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """
    Model configuration.
    """

    backbone: BackboneName = BackboneName.MOBILENET_V2
    strategy: TransferLearningStrategy = TransferLearningStrategy.FEATURE_EXTRACTION
    pretrained: bool = True


@dataclass(frozen=True, slots=True)
class TrainingConfig:
    """
    Training configuration.
    """

    epochs: int = 50
    batch_size: int = 32
    learning_rate: float = 0.001
    optimizer: OptimizerName = OptimizerName.ADAM


@dataclass(frozen=True, slots=True)
class EvaluationConfig:
    """
    Evaluation configuration.
    """

    metrics: tuple[MetricName, ...] = field(
        default=(
            MetricName.ACCURACY,
            MetricName.PRECISION,
            MetricName.RECALL,
            MetricName.F1_SCORE,
        )
    )


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    """
    Complete experiment configuration.
    """

    dataset: DatasetConfig = DatasetConfig()
    model: ModelConfig = ModelConfig()
    training: TrainingConfig = TrainingConfig()
    evaluation: EvaluationConfig = EvaluationConfig()


experiment = ExperimentConfig()
