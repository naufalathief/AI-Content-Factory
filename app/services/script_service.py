import json
import os

from app.db import get_db
from app.models import Video
from app.schemas import Script
from app.script_generator import generate_script


def run(video_id: int):
    with get_db() as db:
        video = db.get(Video, video_id)

        if video is None:
            raise ValueError(f"Video {video_id} not found.")

        script = Script.from_dict(
            generate_script(video.topic)
        )

        os.makedirs(
            "storage/scripts",
            exist_ok=True,
        )

        output = f"storage/scripts/{video.id}.json"

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                script.to_dict(),
                file,
                indent=4,
                ensure_ascii=False,
            )

        video.script_path = output
        video.status = "scripted"

        db.commit()

        return output
