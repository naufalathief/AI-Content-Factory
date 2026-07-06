"""
Dataset module manager.

This module manages train, validation,
and test dataset splits.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.datasets.base_dataset import BaseFERDataset


@dataclass(
    frozen=True,
    slots=True,
)
class FERDataModule:
    """
    FER dataset container.
    """

    train_dataset: BaseFERDataset
    validation_dataset: BaseFERDataset
    test_dataset: BaseFERDataset

    batch_size: int = 32

    @property
    def num_classes(
        self,
    ) -> int:
        """
        Return number of classes.
        """

        return self.train_dataset.num_classes

    @property
    def class_names(
        self,
    ) -> tuple[str, ...]:
        """
        Return class labels.
        """

        return self.train_dataset.class_names
