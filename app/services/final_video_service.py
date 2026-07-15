import os

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

        if not video.video_path:

            raise ValueError(
                "Video path is empty."
            )

        video_path = video.video_path

        subtitle_path = (
            f"storage/subtitles/{video.id}.srt"
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

        os.makedirs(
            "storage/videos",
            exist_ok=True,
        )

        output = (
            f"storage/videos/{video.id}_final.mp4"
        )

        print("=" * 60)
        print("BURN SUBTITLE")
        print("=" * 60)

        burn_subtitle(
            video_path,
            f"storage/voices/{video.id}.mp3",
            subtitle_path,
            output,
        )

        video.final_video_path = output
        video.status = "completed"

        db.commit()

        print("Final video created.")
        print(output)

        return output