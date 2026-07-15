from app.motion.config import MotionConfig


PUSH_IN = MotionConfig(
    name="push_in",
    zoom_start=1.00,
    zoom_end=1.18,
    x_start=0,
    x_end=0,
    y_start=0,
    y_end=0,
)

PUSH_OUT = MotionConfig(
    name="push_out",
    zoom_start=1.18,
    zoom_end=1.00,
    x_start=0,
    x_end=0,
    y_start=0,
    y_end=0,
)

PAN_LEFT = MotionConfig(
    name="pan_left",
    zoom_start=1.10,
    zoom_end=1.10,
    x_start=140,
    x_end=-140,
    y_start=0,
    y_end=0,
)

PAN_RIGHT = MotionConfig(
    name="pan_right",
    zoom_start=1.10,
    zoom_end=1.10,
    x_start=-140,
    x_end=140,
    y_start=0,
    y_end=0,
)

PAN_UP = MotionConfig(
    name="pan_up",
    zoom_start=1.08,
    zoom_end=1.08,
    x_start=0,
    x_end=0,
    y_start=120,
    y_end=-120,
)

PAN_DOWN = MotionConfig(
    name="pan_down",
    zoom_start=1.08,
    zoom_end=1.08,
    x_start=0,
    x_end=0,
    y_start=-120,
    y_end=120,
)

DRIFT_LEFT = MotionConfig(
    name="drift_left",
    zoom_start=1.02,
    zoom_end=1.10,
    x_start=60,
    x_end=-60,
    y_start=-20,
    y_end=20,
)

DRIFT_RIGHT = MotionConfig(
    name="drift_right",
    zoom_start=1.02,
    zoom_end=1.10,
    x_start=-60,
    x_end=60,
    y_start=20,
    y_end=-20,
)

DIAGONAL_UL = MotionConfig(
    name="diagonal_ul",
    zoom_start=1.04,
    zoom_end=1.15,
    x_start=100,
    x_end=-100,
    y_start=100,
    y_end=-100,
)

DIAGONAL_DR = MotionConfig(
    name="diagonal_dr",
    zoom_start=1.04,
    zoom_end=1.15,
    x_start=-100,
    x_end=100,
    y_start=-100,
    y_end=100,
)

ORBIT = MotionConfig(
    name="orbit",
    zoom_start=1.10,
    zoom_end=1.18,
    x_start=40,
    x_end=-40,
    y_start=-40,
    y_end=40,
)

SHAKE = MotionConfig(
    name="shake",
    zoom_start=1.15,
    zoom_end=1.18,
    x_start=0,
    x_end=0,
    y_start=0,
    y_end=0,
    shake_strength=8,
)

ALL_PRESETS = [
    PUSH_IN,
    PUSH_OUT,
    PAN_LEFT,
    PAN_RIGHT,
    PAN_UP,
    PAN_DOWN,
    DRIFT_LEFT,
    DRIFT_RIGHT,
    DIAGONAL_UL,
    DIAGONAL_DR,
    ORBIT,
    SHAKE,
]