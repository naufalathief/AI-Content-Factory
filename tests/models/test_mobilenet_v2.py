"""Tests for MobileNetV2 transfer learning model."""

import torch
from torch import nn

from src.constants.models import TransferLearningStrategy
from src.models.mobilenet_v2 import MobileNetV2TransferLearning


def test_create_mobilenet_v2_model() -> None:
    """Test MobileNetV2 model creation."""

    model = MobileNetV2TransferLearning(
        strategy=TransferLearningStrategy.FEATURE_EXTRACTION,
        num_classes=7,
        pretrained=False,
    )

    assert isinstance(model, MobileNetV2TransferLearning)


def test_forward_pass() -> None:
    """Test MobileNetV2 forward propagation."""

    model = MobileNetV2TransferLearning(
        strategy=TransferLearningStrategy.FEATURE_EXTRACTION,
        num_classes=7,
        pretrained=False,
    )

    inputs = torch.randn(
        2,
        1,
        48,
        48,
    )

    outputs = model(inputs)

    assert outputs.shape == (
        2,
        7,
    )


def test_input_channel_adaptation() -> None:
    """Test grayscale input adaptation."""

    model = MobileNetV2TransferLearning(
        strategy=TransferLearningStrategy.FEATURE_EXTRACTION,
        num_classes=7,
        input_channels=1,
        pretrained=False,
    )

    first_conv = model.backbone.features[0][0]

    assert first_conv.in_channels == 1


def test_classifier_replacement() -> None:
    """Test classifier output replacement."""

    model = MobileNetV2TransferLearning(
        strategy=TransferLearningStrategy.FEATURE_EXTRACTION,
        num_classes=7,
        pretrained=False,
    )

    classifier = model.backbone.classifier[1]

    assert isinstance(
        classifier,
        nn.Linear,
    )

    assert classifier.out_features == 7


def test_feature_extraction_freezing() -> None:
    """Test feature extraction strategy."""

    model = MobileNetV2TransferLearning(
        strategy=TransferLearningStrategy.FEATURE_EXTRACTION,
        num_classes=7,
        pretrained=False,
    )

    feature_parameters = list(model.backbone.features.parameters())

    assert all(not parameter.requires_grad for parameter in feature_parameters)

    classifier_parameters = list(model.backbone.classifier.parameters())

    assert all(parameter.requires_grad for parameter in classifier_parameters)


def test_partial_fine_tuning_freezing() -> None:
    """Test partial fine tuning strategy."""

    model = MobileNetV2TransferLearning(
        strategy=TransferLearningStrategy.PARTIAL_FINE_TUNING,
        num_classes=7,
        pretrained=False,
    )

    for index, layer in enumerate(model.backbone.features):
        for parameter in layer.parameters():
            if index <= 13:
                assert not parameter.requires_grad

            else:
                assert parameter.requires_grad


def test_full_fine_tuning() -> None:
    """Test full fine tuning strategy."""

    model = MobileNetV2TransferLearning(
        strategy=TransferLearningStrategy.FULL_FINE_TUNING,
        num_classes=7,
        pretrained=False,
    )

    assert all(parameter.requires_grad for parameter in model.parameters())
