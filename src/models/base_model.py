"""
Base model module.

This module defines the abstract model interface
for Facial Expression Recognition architectures.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import torch
from torch.nn import Module


class BaseFERModel(
    Module,
    ABC,
):
    """
    Abstract FER model.
    """

    @abstractmethod
    def forward(
        self,
        inputs: torch.Tensor,
    ) -> torch.Tensor:
        """
        Forward propagation.

        Args:
            inputs: Input image tensor.

        Returns:
            Prediction logits.
        """

    @abstractmethod
    def freeze_backbone(
        self,
    ) -> None:
        """
        Freeze feature extractor layers.
        """

    @abstractmethod
    def unfreeze_backbone(
        self,
    ) -> None:
        """
        Unfreeze feature extractor layers.
        """
