import math
import os
import subprocess
from pathlib import Path


def get_audio_duration(audio_path: str) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            audio_path,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return float(result.stdout.strip())


def get_video_files(asset_folder: str):
    return sorted(
        [
            str(path)
            for path in Path(asset_folder).glob("*.mp4")
        ]
    )


def compose_video(
    audio_path: str,
    asset_folder: str,
    output_path: str,
):
    duration = get_audio_duration(audio_path)

    videos = get_video_files(asset_folder)

    if not videos:
        raise RuntimeError("No asset videos found.")

    clip_duration = math.ceil(duration / len(videos))

    temp_dir = Path(asset_folder) / "temp"

    temp_dir.mkdir(
        exist_ok=True,
    )

    trimmed = []

    for index, video in enumerate(videos):

        output = temp_dir / f"{index:03}.mp4"

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video,
                "-t",
                str(clip_duration),
                "-vf",
                "scale=1920:1080,fps=30",
                "-an",
                str(output),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        trimmed.append(output)

    concat = temp_dir / "concat.txt"

    with open(
        concat,
        "w",
        encoding="utf-8",
    ) as file:

        for clip in trimmed:

            file.write(
                f"file '{clip.resolve()}'\n"
            )

    merged = temp_dir / "merged.mp4"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(merged),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    os.makedirs(
        Path(output_path).parent,
        exist_ok=True,
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(merged),
            "-i",
            audio_path,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            output_path,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )

    print("Video exported:", output_path)
