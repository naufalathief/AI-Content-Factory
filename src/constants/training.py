"""
Training-related constants.

This module defines supported training components.
"""

from __future__ import annotations

from enum import StrEnum


class OptimizerName(StrEnum):
    """
    Supported optimizers.
    """

    ADAM = "adam"
    ADAMW = "adamw"
    SGD = "sgd"


class SchedulerName(StrEnum):
    """
    Supported learning rate schedulers.
    """

    NONE = "none"
    STEP = "step"
    COSINE = "cosine"


class DeviceType(StrEnum):
    """
    Supported computation devices.
    """

    AUTO = "auto"
    CPU = "cpu"
    CUDA = "cuda"


class TrainingMode(StrEnum):
    """
    Supported training execution modes.
    """

    TRAIN = "train"
    VALIDATION = "validation"
    TEST = "test"
