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

    assert OptimizerName.ADAM.value == "adam"
    assert OptimizerName.ADAMW.value == "adamw"
    assert OptimizerName.SGD.value == "sgd"


def test_scheduler_names() -> None:
    """
    Scheduler constants should have correct values.
    """

    assert SchedulerName.NONE.value == "none"
    assert SchedulerName.STEP.value == "step"
    assert SchedulerName.COSINE.value == "cosine"


def test_device_types() -> None:
    """
    Device constants should have correct values.
    """

    assert DeviceType.AUTO.value == "auto"
    assert DeviceType.CPU.value == "cpu"
    assert DeviceType.CUDA.value == "cuda"


def test_training_modes() -> None:
    """
    Training modes should have correct values.
    """

    assert TrainingMode.TRAIN.value == "train"
    assert TrainingMode.VALIDATION.value == "validation"
    assert TrainingMode.TEST.value == "test"
