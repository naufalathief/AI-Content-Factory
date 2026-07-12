import json
import os
import subprocess


def file_exists(path):
    return os.path.exists(path)


def get_video_info(path):

    result = subprocess.run(
        [
            "ffprobe",
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


def get_duration(info):
    return float(info["format"]["duration"])


def get_resolution(info):

    for stream in info["streams"]:

        if stream["codec_type"] == "video":

            return (
                stream["width"],
                stream["height"],
            )

    return None


def get_fps(info):

    for stream in info["streams"]:

        if stream["codec_type"] == "video":

            num, den = stream["r_frame_rate"].split("/")

            return round(
                float(num) / float(den),
                2,
            )

    return 0
