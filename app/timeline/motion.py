"""Ken Burns motion presets, rendered by Remotion (renderer/src/video.tsx).

Offsets are in output pixels. The renderer clamps them to the margin the
zoom creates, so a pan can never reveal the black background.
"""

import random
from dataclasses import asdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Motion:

    name: str

    zoomStart: float

    zoomEnd: float

    xStart: float = 0

    xEnd: float = 0

    yStart: float = 0

    yEnd: float = 0

    def to_dict(self) -> dict:
        return asdict(self)


PRESETS = [
    Motion("push_in", 1.00, 1.18),
    Motion("push_out", 1.18, 1.00),
    Motion("pan_left", 1.12, 1.12, 60, -60),
    Motion("pan_right", 1.12, 1.12, -60, 60),
    Motion("pan_up", 1.10, 1.10, 0, 0, 90, -90),
    Motion("pan_down", 1.10, 1.10, 0, 0, -90, 90),
    Motion("drift_left", 1.04, 1.12, 50, -50, -20, 20),
    Motion("drift_right", 1.04, 1.12, -50, 50, 20, -20),
    Motion("diagonal_ul", 1.06, 1.16, 50, -50, 80, -80),
    Motion("diagonal_dr", 1.06, 1.16, -50, 50, -80, 80),
]


class MotionSelector:
    """Random presets without repeating the previous one.

    Seeded with the video id, so re-rendering a video gives the same motion.
    """

    def __init__(self, seed: int):
        self._random = random.Random(seed)
        self._previous: Motion | None = None

    def select(self) -> Motion:

        motion = self._random.choice(
            [preset for preset in PRESETS if preset != self._previous]
        )

        self._previous = motion

        return motion
