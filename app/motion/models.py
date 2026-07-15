from dataclasses import dataclass, field


@dataclass(slots=True)
class MotionFilter:

    name: str

    expression: str


@dataclass(slots=True)
class MotionClip:

    input_index: int

    image_path: str

    duration: float

    output_label: str

    filters: list[MotionFilter] = field(
        default_factory=list,
    )