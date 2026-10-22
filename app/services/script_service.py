import json

from app import settings
from app.db import get_db
from app.models import Video
from app.schemas import Script
from app.generators.script_generator import generate_script


def run(video_id: int):
    with get_db() as db:
        video = db.get(Video, video_id)

        if video is None:
            raise ValueError(f"Video {video_id} not found.")

        script = Script.from_dict(
            generate_script(video.topic)
        )

        output = settings.script_file(video.id)

        output.parent.mkdir(parents=True, exist_ok=True)

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

        video.script_path = str(output)
        video.status = "scripted"

        db.commit()

        return str(output)
