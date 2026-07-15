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


def check(
    name: str,
    status: bool,
) -> bool:

    icon = "✓" if status else "✗"

    print(f"{icon} {name}")

    return status


def run(
    video_id: int,
) -> bool:

    passed = True

    with get_db() as db:

        video = db.get(
            Video,
            video_id,
        )

        if video is None:
            raise ValueError(
                f"Video {video_id} not found."
            )

        script = video.script_path

        voice = video.voice_path

        video_file = video.video_path

        final_video = video.final_video_path

        if not final_video:
            raise ValueError(
                "Final video path is empty."
            )
        
        image_folder = (
            f"storage/images/{video.id}"
        )

        image_metadata = (
            f"{image_folder}/metadata.json"
        )

        subtitle = (
            f"storage/subtitles/{video.id}.srt"
        )

        metadata = (
            f"storage/metadata/{video.id}.json"
        )

        passed &= check(
            "Script",
            file_exists(script),
        )

        passed &= check(
            "Voice",
            file_exists(voice),
        )

        passed &= check(
            "Images",
            os.path.isdir(
                image_folder,
            ),
        )

        passed &= check(
            "Image Metadata",
            file_exists(
                image_metadata,
            ),
        )

        passed &= check(
            "Video",
            file_exists(
                video_file,
            ),
        )

        passed &= check(
            "Subtitle",
            file_exists(
                subtitle,
            ),
        )

        passed &= check(
            "Final Video",
            file_exists(
                final_video,
            ),
        )

        passed &= check(
            "Metadata",
            file_exists(
                metadata,
            ),
        )

        if file_exists(
            final_video,
        ):

            info = get_video_info(
                final_video,
            )

            duration = get_duration(
                info,
            )

            width, height = get_resolution(
                info,
            )

            fps = get_fps(
                info,
            )

            passed &= check(
                "Duration >= 10 sec",
                duration >= 10,
            )

            passed &= check(
                "Resolution 1080x1920",
                width == 1080
                and height == 1920,
            )

            passed &= check(
                "FPS 30",
                abs(fps - 30) < 0.5,
            )

        print()
        print("=" * 60)

        if passed:

            print("QC PASSED")

        else:

            print("QC FAILED")

        print("=" * 60)

        return passed