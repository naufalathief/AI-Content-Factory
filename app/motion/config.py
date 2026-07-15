from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class MotionConfig:
    """
    Configuration for a single camera motion preset.
    """

    name: str

    zoom_start: float
    zoom_end: float

    x_start: float
    x_end: float

    y_start: float
    y_end: float

    speed: float = 1.0

    shake_strength: float = 0.0

    rotation: float = 0.0