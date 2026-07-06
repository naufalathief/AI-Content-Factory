"""
FERPlus dataset tests.
"""

from pathlib import Path

from src.datasets.ferplus import FERPlusDataset


def test_ferplus_loading(
    tmp_path: Path,
) -> None:
    file = tmp_path / "ferplus.csv"

    file.write_text(
        ("image_name,neutral,happiness\nimg.png,1,9\n"),
        encoding="utf-8",
    )

    dataset = FERPlusDataset(
        file,
    )

    assert len(dataset) == 1
    assert dataset.num_classes == 8
