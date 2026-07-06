"""
FERPlus dataset module.

This module implements FERPlus dataset loading.
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.datasets.base_dataset import BaseFERDataset
from src.exceptions.dataset import (
    DatasetNotFoundError,
    InvalidDatasetFormatError,
)


class FERPlusDataset(BaseFERDataset):
    """
    FERPlus dataset implementation.
    """

    def __init__(
        self,
        csv_path: Path,
    ) -> None:
        super().__init__(
            csv_path.parent,
        )

        if not csv_path.exists():
            raise DatasetNotFoundError(f"Dataset file not found: {csv_path}")

        self.csv_path = csv_path
        self.samples = self._load_csv()

    def _load_csv(
        self,
    ) -> list[dict[str, str]]:
        """
        Load FERPlus annotation file.
        """

        with self.csv_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            if "image_name" not in (reader.fieldnames or []):
                raise InvalidDatasetFormatError("Invalid FERPlus format")

            return list(reader)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(
        self,
        index: int,
    ) -> tuple[str, int]:
        sample = self.samples[index]

        image_name = sample["image_name"]

        emotion_votes = {
            key: int(value) for key, value in sample.items() if key != "image_name"
        }

        label = max(
            emotion_votes,
            key=lambda emotion: emotion_votes[emotion],
        )

        return (
            image_name,
            self.class_names.index(label),
        )

    @property
    def num_classes(self) -> int:
        return 8

    @property
    def class_names(
        self,
    ) -> tuple[str, ...]:
        return (
            "neutral",
            "happiness",
            "surprise",
            "sadness",
            "anger",
            "disgust",
            "fear",
            "contempt",
        )
