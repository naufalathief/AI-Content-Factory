import json

from app import settings
from app.db import get_db
from app.generators.metadata_generator import generate_metadata
from app.models import Video


def run(video_id: int):

    with get_db() as db:

        video = db.get(
            Video,
            video_id,
        )

        if video is None:
            raise ValueError("Video not found.")

        with open(
            video.script_path or settings.script_file(video.id),
            "r",
            encoding="utf-8",
        ) as file:

            script = json.load(file)

        metadata = generate_metadata(
            script,
        )

        output = settings.metadata_file(video.id)

        output.parent.mkdir(parents=True, exist_ok=True)

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
                ensure_ascii=False,
            )
        
        video.metadata_path = str(output)

        db.commit()

        return str(output)
