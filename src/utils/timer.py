"""
Timer utility.

This module provides execution time measurement utilities.
"""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(slots=True)
class Timer:
    """
    Simple execution timer.
    """

    start_time: float = 0.0
    end_time: float = 0.0

    def start(self) -> None:
        """
        Start timer.
        """

        self.start_time = time.perf_counter()

    def stop(self) -> None:
        """
        Stop timer.
        """

        self.end_time = time.perf_counter()

    @property
    def elapsed(self) -> float:
        """
        Get elapsed time.

        Returns:
            Elapsed seconds.
        """

        return self.end_time - self.start_time
