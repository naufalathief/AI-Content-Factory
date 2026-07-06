"""MobileNetV2 transfer learning model implementation.

This module provides MobileNetV2 architecture adaptation for
Facial Expression Recognition transfer learning experiments.
"""

from __future__ import annotations

from typing import cast

import torch
from torch import nn
from torch.nn.common_types import _size_2_t
from torchvision.models import (
    MobileNet_V2_Weights,
    MobileNetV2,
    mobilenet_v2,
)

from src.constants.models import TransferLearningStrategy
from src.models.base_model import BaseFERModel


class MobileNetV2TransferLearning(BaseFERModel):
    """MobileNetV2 model for transfer learning experiments.

    This class adapts ImageNet pretrained MobileNetV2 for
    Facial Expression Recognition tasks by modifying the input
    convolution layer, replacing the classifier, and applying
    different transfer learning strategies.

    Args:
        strategy:
            Transfer learning strategy.
        num_classes:
            Number of output emotion classes.
        input_channels:
            Number of image input channels.
        pretrained:
            Whether to use ImageNet pretrained weights.
    """

    def __init__(
        self,
        strategy: TransferLearningStrategy,
        num_classes: int,
        input_channels: int = 1,
        pretrained: bool = True,
    ) -> None:
        super().__init__()

        self.strategy = strategy
        self.num_classes = num_classes
        self.input_channels = input_channels
        self.pretrained = pretrained

        self.backbone = self._load_backbone()

        self._adapt_input_conv()
        self._replace_classifier()
        self._apply_strategy()

    def _load_backbone(self) -> MobileNetV2:
        """Load MobileNetV2 backbone."""

        weights = MobileNet_V2_Weights.IMAGENET1K_V1 if self.pretrained else None

        model = mobilenet_v2(
            weights=weights,
        )

        return cast(
            MobileNetV2,
            model,
        )

    def _adapt_input_conv(self) -> None:
        """Adapt first convolution layer for grayscale input."""

        if self.input_channels == 3:
            return

        old_conv = cast(
            nn.Conv2d,
            self.backbone.features[0][0],
        )

        new_conv = nn.Conv2d(
            in_channels=self.input_channels,
            out_channels=old_conv.out_channels,
            kernel_size=cast(
                _size_2_t,
                old_conv.kernel_size,
            ),
            stride=cast(
                _size_2_t,
                old_conv.stride,
            ),
            padding=cast(
                _size_2_t | str,
                old_conv.padding,
            ),
            bias=old_conv.bias is not None,
        )

        if self.pretrained and self.input_channels == 1:
            with torch.no_grad():
                new_conv.weight.copy_(
                    old_conv.weight.mean(
                        dim=1,
                        keepdim=True,
                    )
                )

        self.backbone.features[0][0] = new_conv

    def _replace_classifier(self) -> None:
        """Replace ImageNet classifier with FER classifier."""

        old_classifier = cast(
            nn.Linear,
            self.backbone.classifier[1],
        )

        in_features = old_classifier.in_features

        self.backbone.classifier[1] = nn.Linear(
            in_features,
            self.num_classes,
        )

    def _apply_strategy(self) -> None:
        """Apply selected transfer learning strategy."""

        if self.strategy == TransferLearningStrategy.FEATURE_EXTRACTION:
            self._freeze_feature_extractor()

        elif self.strategy == TransferLearningStrategy.PARTIAL_FINE_TUNING:
            self._freeze_partial_layers()

        elif self.strategy == TransferLearningStrategy.FULL_FINE_TUNING:
            self.unfreeze_backbone()

    def _freeze_feature_extractor(self) -> None:
        """Apply feature extraction freezing."""

        self.freeze_backbone()

    def _freeze_partial_layers(self) -> None:
        """Freeze early MobileNetV2 feature layers."""

        for index, layer in enumerate(self.backbone.features):
            requires_grad = index > 13

            for parameter in layer.parameters():
                parameter.requires_grad = requires_grad

    def freeze_backbone(self) -> None:
        """Freeze MobileNetV2 backbone."""

        for parameter in self.backbone.features.parameters():
            parameter.requires_grad = False

    def unfreeze_backbone(self) -> None:
        """Unfreeze MobileNetV2 backbone."""

        for parameter in self.backbone.features.parameters():
            parameter.requires_grad = True

    def forward(
        self,
        inputs: torch.Tensor,
    ) -> torch.Tensor:
        """Perform forward propagation."""

        return cast(
            torch.Tensor,
            self.backbone(inputs),
        )
