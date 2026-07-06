"""
Image transformation module.

This module defines preprocessing configuration
for FER experiments.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class TransformConfig:
    """
    Image transformation configuration.
    """

    image_size: int = 224
    normalize: bool = True
    augment: bool = False


def create_transform_config(
    image_size: int = 224,
    normalize: bool = True,
    augment: bool = False,
) -> TransformConfig:
    """
    Create transformation configuration.

    Args:
        image_size: Target image size.
        normalize: Enable normalization.
        augment: Enable augmentation.

    Returns:
        Transform configuration.
    """

    return TransformConfig(
        image_size=image_size,
        normalize=normalize,
        augment=augment,
    )
