"""
Framework exceptions package.
"""

from src.exceptions.base import FERFrameworkError
from src.exceptions.config import ConfigError
from src.exceptions.dataset import (
    DatasetError,
    DatasetNotFoundError,
    InvalidDatasetFormatError,
)
from src.exceptions.model import (
    ModelError,
    UnsupportedModelError,
)
from src.exceptions.training import (
    CheckpointError,
    TrainingError,
)

__all__ = [
    "FERFrameworkError",
    "ConfigError",
    "DatasetError",
    "DatasetNotFoundError",
    "InvalidDatasetFormatError",
    "ModelError",
    "UnsupportedModelError",
    "TrainingError",
    "CheckpointError",
]
