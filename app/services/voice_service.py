import json

from app import settings
from app.db import get_db
from app.generators.voice_generator import generate_voice
from app.models import Video
from app.schemas import Script


def run(video_id: int):
    with get_db() as db:

        video = db.get(Video, video_id)

        if video is None:
            raise ValueError(f"Video {video_id} not found.")

        script_path = video.script_path or str(
            settings.script_file(video.id)
        )

        with open(
            script_path,
            "r",
            encoding="utf-8",
        ) as file:

            script = Script.from_dict(
                json.load(file)
            )

        text = "\n\n".join(script.narration())

        output = settings.voice_file(video.id)

        generate_voice(
            text,
            output,
            settings.words_file(video.id),
        )

        video.voice_path = str(output)
        video.status = "voiced"

        db.commit()

        return str(output)
