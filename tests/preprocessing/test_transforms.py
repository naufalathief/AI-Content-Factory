"""
Unit tests for image transformations.
"""

from src.preprocessing.transforms import (
    TransformConfig,
    create_transform_config,
)


def test_default_transform_config() -> None:
    """
    Default transform should be valid.
    """

    config = create_transform_config()

    assert isinstance(
        config,
        TransformConfig,
    )

    assert config.image_size == 224
    assert config.normalize is True
    assert config.augment is False


def test_custom_transform_config() -> None:
    """
    Custom transform should override defaults.
    """

    config = create_transform_config(
        image_size=48,
        augment=True,
    )

    assert config.image_size == 48
    assert config.augment is True
