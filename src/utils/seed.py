"""
Random seed utility.

This module provides reproducibility utilities
for machine learning experiments.
"""

from __future__ import annotations

import os
import random


def set_seed(
    seed: int,
) -> None:
    """
    Set random seed globally.

    Args:
        seed: Random seed value.
    """

    random.seed(seed)

    os.environ["PYTHONHASHSEED"] = str(seed)
