import random

from app.motion.config import MotionConfig
from app.motion.presets import ALL_PRESETS


class MotionSelector:

    def __init__(self):

        self._previous: MotionConfig | None = None

    def select(self) -> MotionConfig:

        candidates = [

            preset

            for preset in ALL_PRESETS

            if preset != self._previous

        ]

        motion = random.choice(
            candidates
        )

        self._previous = motion

        return motion

    def reset(self):

        self._previous = None