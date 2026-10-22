import json
from pathlib import Path

from app import settings
from app.db import get_db
from app.generators.subtitle_generator import generate_subtitle
from app.models import Video
from app.schemas import Script


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

        voice = Path(
            video.voice_path or settings.voice_file(video.id)
        )

        if not voice.exists():
            raise FileNotFoundError(voice)

        text = None

        script_path = Path(
            video.script_path or settings.script_file(video.id)
        )

        if script_path.exists():

            script = Script.from_dict(
                json.loads(script_path.read_text(encoding="utf-8"))
            )

            text = " ".join(script.narration())

        output = settings.subtitle_file(video.id)

        generate_subtitle(
            voice,
            output,
            words_path=settings.words_file(video.id),
            text=text,
        )

        return str(output)
