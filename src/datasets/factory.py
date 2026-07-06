"""
Dataset factory module.
"""

from __future__ import annotations

from pathlib import Path

from src.constants.datasets import DatasetName
from src.datasets.base_dataset import BaseFERDataset
from src.datasets.fer2013 import FER2013Dataset
from src.datasets.ferplus import FERPlusDataset
from src.exceptions.dataset import InvalidDatasetFormatError


def create_dataset(
    name: DatasetName,
    path: Path,
) -> BaseFERDataset:
    """
    Create dataset instance.
    """

    match name:
        case DatasetName.FER2013:
            return FER2013Dataset(
                path,
            )

        case DatasetName.FERPLUS:
            return FERPlusDataset(
                path,
            )

        case _:
            raise InvalidDatasetFormatError(f"Unsupported dataset: {name}")
