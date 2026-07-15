import json
from pathlib import Path

from app.generators.image_generator import ImageGenerator
from app.schemas import Script
from app.db import get_db
from app.models import Video


def run(video_id: int):

    script_path = Path(
        f"storage/scripts/{video_id}.json"
    )

    if not script_path.exists():

        raise FileNotFoundError(
            script_path
        )

    with open(
        script_path,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    script = Script.from_dict(
        data
    )

    generator = ImageGenerator()

    generator.generate(
        video_id,
        script,
    )

    with get_db() as db:

        video = db.get(
            Video,
            video_id,
        )

        if video is None:
            raise ValueError(
                f"Video {video_id} not found."
            )

        video.status = "images_generated"

        db.commit()

    return (
        f"storage/images/{video_id}"
    )