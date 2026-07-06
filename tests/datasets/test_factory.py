"""
Dataset factory tests.
"""

from pathlib import Path

from src.constants.datasets import DatasetName
from src.datasets.factory import create_dataset
from src.datasets.fer2013 import FER2013Dataset


def test_create_fer2013(
    tmp_path: Path,
) -> None:
    file = tmp_path / "fer.csv"

    file.write_text(
        ("emotion,pixels\n0,1 2 3\n"),
        encoding="utf-8",
    )

    dataset = create_dataset(
        DatasetName.FER2013,
        file,
    )

    assert isinstance(
        dataset,
        FER2013Dataset,
    )
