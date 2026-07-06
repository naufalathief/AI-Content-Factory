"""
Unit tests for the path configuration module.
"""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from src.config.paths import PathSettings, paths


def test_project_root_exists() -> None:
    """
    Project root directory should exist.
    """
    assert paths.project_root.exists()


def test_all_directories_are_path_objects() -> None:
    """
    Every configured directory should be a pathlib.Path object.
    """
    attributes = (
        paths.project_root,
        paths.configs_dir,
        paths.data_dir,
        paths.raw_data_dir,
        paths.processed_data_dir,
        paths.cache_dir,
        paths.external_data_dir,
        paths.docs_dir,
        paths.notebooks_dir,
        paths.outputs_dir,
        paths.checkpoints_dir,
        paths.logs_dir,
        paths.predictions_dir,
        paths.reports_dir,
        paths.figures_dir,
        paths.metrics_dir,
        paths.tables_dir,
        paths.src_dir,
        paths.tests_dir,
    )

    assert all(isinstance(attribute, Path) for attribute in attributes)


def test_output_directory_structure() -> None:
    """
    Output directories should be resolved correctly.
    """
    assert paths.logs_dir == paths.outputs_dir / "logs"
    assert paths.checkpoints_dir == paths.outputs_dir / "checkpoints"
    assert paths.predictions_dir == paths.outputs_dir / "predictions"
    assert paths.reports_dir == paths.outputs_dir / "reports"


def test_create_directories() -> None:
    """
    Output directories should exist after initialization.
    """
    paths.create_directories()

    assert paths.outputs_dir.exists()
    assert paths.logs_dir.exists()
    assert paths.checkpoints_dir.exists()
    assert paths.predictions_dir.exists()
    assert paths.reports_dir.exists()
    assert paths.figures_dir.exists()
    assert paths.metrics_dir.exists()
    assert paths.tables_dir.exists()


def test_path_settings_immutable() -> None:
    """
    PathSettings should be immutable.
    """
    with pytest.raises(FrozenInstanceError):
        paths.project_root = Path.cwd()  # type: ignore[misc]


def test_singleton_instance() -> None:
    """
    Imported singleton should be an instance of PathSettings.
    """
    assert isinstance(paths, PathSettings)
