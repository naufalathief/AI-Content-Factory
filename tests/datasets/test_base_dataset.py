"""
Unit tests for base dataset.
"""

from pathlib import Path
from typing import Any

from src.datasets.base_dataset import BaseFERDataset


class DummyDataset(BaseFERDataset):
    """
    Dummy dataset implementation.
    """

    def __len__(self) -> int:
        return 10

    def __getitem__(
        self,
        index: int,
    ) -> tuple[Any, int]:
        return index, 0

    @property
    def num_classes(self) -> int:
        return 7

    @property
    def class_names(
        self,
    ) -> tuple[str, ...]:
        return (
            "angry",
            "disgust",
            "fear",
            "happy",
            "sad",
            "surprise",
            "neutral",
        )


def test_base_dataset_contract() -> None:
    """
    Dataset contract should work.
    """

    dataset = DummyDataset(Path("dummy"))

    assert len(dataset) == 10
    assert dataset.num_classes == 7

    assert dataset.class_names[0] == "angry"
