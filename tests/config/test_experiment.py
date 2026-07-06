"""
Unit tests for experiment configuration.
"""

from dataclasses import FrozenInstanceError

import pytest

from src.config.experiment import ExperimentConfig, experiment


def test_experiment_instance() -> None:
    """
    Experiment should be initialized.
    """
    assert isinstance(experiment, ExperimentConfig)


def test_dataset_config() -> None:
    """
    Dataset configuration should be valid.
    """
    assert experiment.dataset.image_size > 0
    assert experiment.dataset.num_classes > 0


def test_model_config() -> None:
    """
    Model configuration should be valid.
    """
    assert experiment.model.backbone
    assert experiment.model.strategy


def test_training_config() -> None:
    """
    Training configuration should be valid.
    """
    assert experiment.training.epochs > 0
    assert experiment.training.batch_size > 0
    assert experiment.training.learning_rate > 0


def test_evaluation_config() -> None:
    """
    Evaluation metrics should exist.
    """
    assert len(experiment.evaluation.metrics) > 0


def test_experiment_is_immutable() -> None:
    """
    Experiment config should be immutable.
    """
    with pytest.raises(FrozenInstanceError):
        experiment.training = None  # type: ignore[misc, assignment]
