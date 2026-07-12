import os

from app.db import get_db
from app.models import Video
from app.video_composer import compose_video


def run(video_id: int):
    with get_db() as db:

        video = db.get(Video, video_id)

        if video is None:
            raise ValueError(f"Video {video_id} not found.")

        if not os.path.exists(video.voice_path):
            raise FileNotFoundError(video.voice_path)

        asset_folder = f"storage/assets/{video.id}"

        output = f"storage/videos/{video.id}.mp4"

        compose_video(
            video.voice_path,
            asset_folder,
            output,
        )

        video.video_path = output
        video.status = "composed"

        db.commit()

        return output
