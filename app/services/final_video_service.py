import os

from app.db import get_db
from app.models import Video
from app.video_burner import burn_subtitle


def run(video_id: int):
    with get_db() as db:

        video = db.get(
            Video,
            video_id,
        )

        if video is None:
            raise ValueError("Video not found.")

        video_path = video.video_path

        subtitle_path = (
            f"storage/subtitles/{video.id}.srt"
        )

        if not os.path.exists(video_path):
            raise FileNotFoundError(video_path)

        if not os.path.exists(subtitle_path):
            raise FileNotFoundError(subtitle_path)

        output = (
            f"storage/videos/{video.id}_final.mp4"
        )

        burn_subtitle(
            video_path,
            subtitle_path,
            output,
        )

        return output
