import os

from app import settings
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

        script = video.script_path or str(settings.script_file(video.id))

        voice = video.voice_path or str(settings.voice_file(video.id))

        video_file = video.video_path or str(settings.video_file(video.id))

        final_video = video.final_video_path or str(
            settings.final_video_file(video.id)
        )

        image_folder = str(settings.image_dir(video.id))

        image_metadata = (
            f"{image_folder}/metadata.json"
        )

        subtitle = str(settings.subtitle_file(video.id))

        metadata = str(settings.metadata_file(video.id))

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

            passed &= check(
                "Duration <= 60 sec (Shorts limit)",
                duration <= 60,
            )

            if file_exists(voice):

                voice_duration = get_duration(get_video_info(voice))

                passed &= check(
                    "Video covers the whole narration",
                    duration + 0.1 >= voice_duration,
                )

        print()
        print("=" * 60)

        if passed:

            video.status = "qc_passed"
            db.commit()

            print("QC PASSED")

        else:

            print("QC FAILED")

        print("=" * 60)

        return passed