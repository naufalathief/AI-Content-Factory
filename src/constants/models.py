"""
Model-related constants.

This module defines supported model architectures and
transfer learning strategies.
"""

from __future__ import annotations

from enum import StrEnum


class BackboneName(StrEnum):
    """
    Supported backbone architectures.
    """

    MOBILENET_V2 = "mobilenet_v2"
    RESNET18 = "resnet18"
    EFFICIENTNET_B0 = "efficientnet_b0"


class TransferLearningStrategy(StrEnum):
    """
    Supported transfer learning strategies.
    """

    FEATURE_EXTRACTION = "feature_extraction"
    PARTIAL_FINE_TUNING = "partial_finetuning"
    FULL_FINE_TUNING = "full_finetuning"
