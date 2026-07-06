"""
Unit tests for seed utilities.
"""

import os
import random

from src.utils.seed import set_seed


def test_set_seed_environment() -> None:
    """
    Seed should update environment variable.
    """

    set_seed(42)

    assert os.environ["PYTHONHASHSEED"] == "42"


def test_set_seed_reproducibility() -> None:
    """
    Random values should be reproducible.
    """

    set_seed(42)

    first = random.random()

    set_seed(42)

    second = random.random()

    assert first == second
