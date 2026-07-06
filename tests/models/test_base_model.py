"""
Unit tests for base FER model.
"""

from torch import nn

from src.models.base_model import BaseFERModel


def test_base_model_inherits_module() -> None:
    """
    Base model should inherit torch module.
    """

    assert issubclass(
        BaseFERModel,
        nn.Module,
    )
