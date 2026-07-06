"""
Unit tests for training constants.
"""

from src.constants.training import (
    DeviceType,
    OptimizerName,
    SchedulerName,
    TrainingMode,
)


def test_optimizer_names() -> None:
    """
    Optimizer constants should have correct values.
    """

    assert OptimizerName.ADAM == "adam"
    assert OptimizerName.ADAMW == "adamw"
    assert OptimizerName.SGD == "sgd"


def test_scheduler_names() -> None:
    """
    Scheduler constants should have correct values.
    """

    assert SchedulerName.NONE == "none"
    assert SchedulerName.STEP == "step"
    assert SchedulerName.COSINE == "cosine"


def test_device_types() -> None:
    """
    Device constants should have correct values.
    """

    assert DeviceType.AUTO == "auto"
    assert DeviceType.CPU == "cpu"
    assert DeviceType.CUDA == "cuda"


def test_training_modes() -> None:
    """
    Training modes should have correct values.
    """

    assert TrainingMode.TRAIN == "train"
    assert TrainingMode.VALIDATION == "validation"
    assert TrainingMode.TEST == "test"
