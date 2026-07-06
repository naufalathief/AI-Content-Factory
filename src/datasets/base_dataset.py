"""
Base dataset module.

This module defines dataset abstraction contract
for Facial Expression Recognition datasets.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseFERDataset(ABC):
    """
    Abstract base class for FER datasets.
    """

    def __init__(
        self,
        root_dir: Path,
    ) -> None:
        """
        Initialize dataset.

        Args:
            root_dir: Dataset root directory.
        """

        self.root_dir = root_dir

    @abstractmethod
    def __len__(self) -> int:
        """
        Return dataset size.
        """

    @abstractmethod
    def __getitem__(
        self,
        index: int,
    ) -> tuple[Any, int]:
        """
        Return dataset item.
        """

    @property
    @abstractmethod
    def num_classes(self) -> int:
        """
        Number of classes.
        """

    @property
    @abstractmethod
    def class_names(
        self,
    ) -> tuple[str, ...]:
        """
        Dataset class labels.
        """
