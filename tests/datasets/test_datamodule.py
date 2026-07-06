"""
Unit tests for FER DataModule.
"""

from pathlib import Path
from typing import Any

from src.datasets.base_dataset import BaseFERDataset
from src.datasets.datamodule import FERDataModule


class DummyDataset(BaseFERDataset):
    """
    Dummy dataset.
    """

    def __len__(
        self,
    ) -> int:
        return 10

    def __getitem__(
        self,
        index: int,
    ) -> tuple[Any, int]:
        return index, 0

    @property
    def num_classes(
        self,
    ) -> int:
        return 7

    @property
    def class_names(
        self,
    ) -> tuple[str, ...]:
        return (
            "angry",
            "happy",
        )


def test_datamodule_creation() -> None:
    """
    DataModule should store datasets.
    """

    dataset = DummyDataset(Path("dummy"))

    module = FERDataModule(
        train_dataset=dataset,
        validation_dataset=dataset,
        test_dataset=dataset,
    )

    assert module.batch_size == 32

    assert len(module.train_dataset) == 10


def test_datamodule_metadata() -> None:
    """
    DataModule should expose metadata.
    """

    dataset = DummyDataset(Path("dummy"))

    module = FERDataModule(
        train_dataset=dataset,
        validation_dataset=dataset,
        test_dataset=dataset,
    )

    assert module.num_classes == 7

    assert module.class_names == (
        "angry",
        "happy",
    )
