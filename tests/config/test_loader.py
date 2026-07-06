"""
Unit tests for configuration loader.
"""

from pathlib import Path

import pytest

from src.config.experiment import ExperimentConfig
from src.config.loader import load_experiment_config


def test_load_experiment_config(
    tmp_path: Path,
) -> None:
    """
    Loader should parse YAML into ExperimentConfig.
    """

    config_file = tmp_path / "config.yaml"

    config_file.write_text(
        """
dataset:
  name: FERPlus
  image_size: 224
  num_classes: 8

model:
  backbone: mobilenet_v2
  strategy: full_finetuning

training:
  epochs: 100
  batch_size: 64

evaluation:
  metrics:
    - accuracy
    - f1_score
""",
        encoding="utf-8",
    )

    config = load_experiment_config(config_file)

    assert isinstance(config, ExperimentConfig)

    assert config.dataset.name == "FERPlus"
    assert config.dataset.num_classes == 8

    assert config.model.strategy == "full_finetuning"

    assert config.training.epochs == 100
    assert config.training.batch_size == 64

    assert "accuracy" in config.evaluation.metrics


def test_missing_config_file() -> None:
    """
    Missing configuration should raise error.
    """

    with pytest.raises(FileNotFoundError):
        load_experiment_config(Path("missing.yaml"))
