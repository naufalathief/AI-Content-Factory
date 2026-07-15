import json
import os
import subprocess
from pathlib import Path

from app.ffmpeg import FFPROBE


def file_exists(path: str | None) -> bool:

    if not path:
        return False

    return Path(path).exists()


def get_video_info(path: str) -> dict:

    if not file_exists(path):
        raise FileNotFoundError(path)

    result = subprocess.run(
        [
            FFPROBE,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(result.stdout)


def get_duration(
    info: dict,
) -> float:

    return float(
        info["format"]["duration"]
    )


def get_resolution(
    info: dict,
) -> tuple[int, int]:

    for stream in info["streams"]:

        if stream["codec_type"] == "video":

            return (
                int(stream["width"]),
                int(stream["height"]),
            )

    raise RuntimeError(
        "Video stream not found."
    )


def get_fps(
    info: dict,
) -> float:

    for stream in info["streams"]:

        if stream["codec_type"] != "video":
            continue

        numerator, denominator = (
            stream["r_frame_rate"].split("/")
        )

        denominator = float(denominator)

        if denominator == 0:
            return 0

        return round(
            float(numerator)
            / denominator,
            2,
        )

    return 0


def is_vertical(
    info: dict,
) -> bool:

    width, height = get_resolution(info)

    return (
        width == 1080
        and height == 1920
    )


def is_horizontal(
    info: dict,
) -> bool:

    width, height = get_resolution(info)

    return (
        width == 1920
        and height == 1080
    )


def is_30fps(
    info: dict,
) -> bool:

    fps = get_fps(info)

    return abs(fps - 30) < 0.5


def has_duration(
    info: dict,
    minimum: float,
) -> bool:

    return (
        get_duration(info)
        >= minimum
    )