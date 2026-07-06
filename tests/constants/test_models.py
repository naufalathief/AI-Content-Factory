"""
Unit tests for model constants.
"""

from src.constants.models import (
    BackboneName,
    TransferLearningStrategy,
)


def test_backbone_values() -> None:
    """
    Backbone constants should have correct values.
    """

    assert BackboneName.MOBILENET_V2 == "mobilenet_v2"
    assert BackboneName.RESNET18 == "resnet18"
    assert BackboneName.EFFICIENTNET_B0 == "efficientnet_b0"


def test_transfer_learning_strategy_values() -> None:
    """
    Transfer learning strategy constants should have correct values.
    """

    assert TransferLearningStrategy.FEATURE_EXTRACTION == "feature_extraction"

    assert TransferLearningStrategy.PARTIAL_FINETUNING == "partial_finetuning"

    assert TransferLearningStrategy.FULL_FINETUNING == "full_finetuning"
