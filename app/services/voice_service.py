import json
import os

from app.db import get_db
from app.models import Video
from app.schemas import Script
from app.generators.voice_generator import generate_voice


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

        text = "\n\n".join(
            scene.text
            for scene in script.scenes
        )

        text += "\n\n"
        text += script.cta

        os.makedirs(
            "storage/voices",
            exist_ok=True,
        )

        output = f"storage/voices/{video.id}.mp3"

        generate_voice(
            text,
            output,
        )

        video.voice_path = output
        video.status = "voiced"

        db.commit()

        return output
