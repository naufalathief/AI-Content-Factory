import os

from app.db import get_db
from app.models import Video
from app.qc import (
    file_exists,
    get_duration,
    get_fps,
    get_resolution,
    get_video_info,
)


def check(name, status):

    icon = "✓" if status else "✗"

    print(f"{icon} {name}")

    return status


def run(video_id):

    passed = True

    with get_db() as db:

        video = db.get(Video, video_id)

        script = video.script_path

        voice = video.voice_path

        assets = f"storage/assets/{video.id}"

        video_file = video.video_path

        subtitle = f"storage/subtitles/{video.id}.srt"

        final = f"storage/videos/{video.id}_final.mp4"

        passed &= check(
            "Script exists",
            file_exists(script),
        )

        passed &= check(
            "Voice exists",
            file_exists(voice),
        )

        passed &= check(
            "Assets exist",
            os.path.isdir(assets),
        )

        passed &= check(
            "Video exists",
            file_exists(video_file),
        )

        passed &= check(
            "Subtitle exists",
            file_exists(subtitle),
        )

        passed &= check(
            "Final video exists",
            file_exists(final),
        )

        if file_exists(final):

            info = get_video_info(final)

            duration = get_duration(info)

            width, height = get_resolution(info)

            fps = get_fps(info)

            passed &= check(
                "Duration > 10 sec",
                duration > 10,
            )

            passed &= check(
                "Resolution 1920x1080",
                width == 1920 and height == 1080,
            )

            passed &= check(
                "FPS 30",
                abs(fps - 30) < 0.5,
            )

        print()

        print("===================")

        if passed:

            print("PASS")

        else:

            print("FAILED")
