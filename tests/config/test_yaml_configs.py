"""
Test real experiment YAML files.
"""

from src.config.loader import load_experiment_config
from src.config.paths import paths


def test_feature_extraction_config() -> None:
    config = load_experiment_config(paths.configs_dir / "feature_extraction.yaml")

    assert config.model.strategy == "feature_extraction"


def test_partial_finetuning_config() -> None:
    config = load_experiment_config(paths.configs_dir / "partial_finetuning.yaml")

    assert config.model.strategy == "partial_finetuning"


def test_full_finetuning_config() -> None:
    config = load_experiment_config(paths.configs_dir / "full_finetuning.yaml")

    assert config.model.strategy == "full_finetuning"
