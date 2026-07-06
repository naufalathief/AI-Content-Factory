"""
Unit tests for FER2013 dataset.
"""

from pathlib import Path

import pytest

from src.datasets.fer2013 import FER2013Dataset
from src.exceptions.dataset import DatasetNotFoundError


def test_fer2013_loading(
    tmp_path: Path,
) -> None:
    """
    FER2013 dataset should load csv.
    """

    file = tmp_path / "fer2013.csv"

    file.write_text(
        ("emotion,pixels,Usage\n0,1 2 3 4,Training\n"),
        encoding="utf-8",
    )

    dataset = FER2013Dataset(
        file,
    )

    assert len(dataset) == 1

    pixels, label = dataset[0]

    assert pixels == "1 2 3 4"
    assert label == 0


def test_missing_dataset() -> None:
    """
    Missing dataset should raise error.
    """

    with pytest.raises(
        DatasetNotFoundError,
    ):
        FER2013Dataset(Path("missing.csv"))
