"""
FER2013 dataset module.

This module implements FER2013 dataset loading logic.
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.constants.datasets import EmotionLabel
from src.datasets.base_dataset import BaseFERDataset
from src.exceptions.dataset import (
    DatasetNotFoundError,
    InvalidDatasetFormatError,
)


class FER2013Dataset(BaseFERDataset):
    """
    FER2013 dataset implementation.
    """

    def __init__(
        self,
        csv_path: Path,
    ) -> None:
        """
        Initialize FER2013 dataset.

        Args:
            csv_path: FER2013 csv file path.
        """

        super().__init__(
            csv_path.parent,
        )

        if not csv_path.exists():
            raise DatasetNotFoundError(f"Dataset file not found: {csv_path}")

        self.csv_path = csv_path

        self.samples = self._load_csv()

    def _load_csv(
        self,
    ) -> list[tuple[str, int]]:
        """
        Load FER2013 csv file.

        Returns:
            List of pixel data and labels.
        """

        samples: list[tuple[str, int]] = []

        with self.csv_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            required_columns = {
                "emotion",
                "pixels",
            }

            if not required_columns.issubset(reader.fieldnames or []):
                raise InvalidDatasetFormatError("Invalid FER2013 format")

            for row in reader:
                samples.append(
                    (
                        row["pixels"],
                        int(row["emotion"]),
                    )
                )

        return samples

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(
        self,
        index: int,
    ) -> tuple[str, int]:
        return self.samples[index]

    @property
    def num_classes(self) -> int:
        return 7

    @property
    def class_names(
        self,
    ) -> tuple[str, ...]:
        return tuple(label.value for label in EmotionLabel)
