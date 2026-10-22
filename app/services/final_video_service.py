import os

from app import settings
from app.db import get_db
from app.models import Video
from app.renderer.video_burner import burn_subtitle


def run(
    video_id: int,
):

    with get_db() as db:

        video = db.get(
            Video,
            video_id,
        )

        if video is None:

            raise ValueError(
                f"Video {video_id} not found."
            )

        # Fall back to the default location so a resumed run (render step
        # skipped because the file exists) still works.
        video_path = video.video_path or str(
            settings.video_file(video.id)
        )

        subtitle_path = str(
            settings.subtitle_file(video.id)
        )

        if not os.path.exists(
            video_path,
        ):

            raise FileNotFoundError(
                video_path,
            )

        if not os.path.exists(
            subtitle_path,
        ):

            raise FileNotFoundError(
                subtitle_path,
            )

        output = str(
            settings.final_video_file(video.id)
        )

        print("=" * 60)
        print("BURN SUBTITLE")
        print("=" * 60)

        burn_subtitle(
            video_path,
            video.voice_path or str(settings.voice_file(video.id)),
            subtitle_path,
            output,
        )

        video.video_path = video_path
        video.final_video_path = output
        video.status = "completed"

        db.commit()

        print("Final video created.")
        print(output)

        return output