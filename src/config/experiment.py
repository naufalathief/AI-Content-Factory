"""
Experiment configuration module.

This module defines experiment-level configuration used for
training and evaluating transfer learning strategies.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DatasetConfig:
    """
    Dataset configuration.

    Attributes:
        name: Dataset name.
        image_size: Input image size.
        num_classes: Number of emotion classes.
    """

    name: str = "FER2013"
    image_size: int = 224
    num_classes: int = 7


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """
    Model configuration.

    Attributes:
        backbone: CNN backbone architecture.
        strategy: Transfer learning strategy.
        pretrained: Use pretrained weights.
    """

    backbone: str = "mobilenet_v2"
    strategy: str = "feature_extraction"
    pretrained: bool = True


@dataclass(frozen=True, slots=True)
class TrainingConfig:
    """
    Training configuration.

    Attributes:
        epochs: Training epochs.
        batch_size: Batch size.
        learning_rate: Optimizer learning rate.
        optimizer: Optimizer name.
    """

    epochs: int = 50
    batch_size: int = 32
    learning_rate: float = 0.001
    optimizer: str = "adam"


@dataclass(frozen=True, slots=True)
class EvaluationConfig:
    """
    Evaluation configuration.

    Attributes:
        metrics: Evaluation metrics.
    """

    metrics: tuple[str, ...] = field(
        default=(
            "accuracy",
            "precision",
            "recall",
            "f1_score",
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
