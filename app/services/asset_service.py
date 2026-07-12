import json

from app.asset_generator import download_assets
from app.db import get_db
from app.models import Video
from app.schemas import Script


def run(video_id: int):
    with get_db() as db:

        video = db.get(Video, video_id)

        if video is None:
            raise ValueError(f"Video {video_id} not found.")

        with open(
            video.script_path,
            "r",
            encoding="utf-8",
        ) as file:

            script = Script.from_dict(
                json.load(file)
            )

        keywords = [
            scene.keyword
            for scene in script.scenes
        ]

        download_assets(
            video.id,
            keywords,
        )

        return f"storage/assets/{video.id}"
