"""
Unit tests for dataset exceptions.
"""

from src.exceptions.dataset import (
    DatasetError,
    DatasetNotFoundError,
    InvalidDatasetFormatError,
)


def test_dataset_exception_hierarchy() -> None:
    """
    Dataset exceptions should inherit DatasetError.
    """

    assert issubclass(
        DatasetNotFoundError,
        DatasetError,
    )

    assert issubclass(
        InvalidDatasetFormatError,
        DatasetError,
    )
