import os

from app.db import get_db
from app.models import Video
from app.subtitle_cleaner import clean_srt
from app.generators.subtitle_generator import generate_subtitle


def run(video_id: int):
    with get_db() as db:

        video = db.get(
            Video,
            video_id,
        )

        if video is None:
            raise ValueError(
                f"Video {video_id} not found."
            )

        if not os.path.exists(video.voice_path):
            raise FileNotFoundError(
                video.voice_path
            )

        os.makedirs(
            "storage/subtitles",
            exist_ok=True,
        )

        raw = (
            f"storage/subtitles/{video.id}_raw.srt"
        )

        clean = (
            f"storage/subtitles/{video.id}.srt"
        )

        generate_subtitle(
            video.voice_path,
            raw,
        )

        clean_srt(
            raw,
            clean,
        )

        return clean
