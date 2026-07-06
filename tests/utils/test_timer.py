"""
Unit tests for timer utilities.
"""

import time

from src.utils.timer import Timer


def test_timer_elapsed() -> None:
    """
    Timer should measure elapsed time.
    """

    timer = Timer()

    timer.start()

    time.sleep(0.01)

    timer.stop()

    assert timer.elapsed > 0
