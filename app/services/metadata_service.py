import json
import os

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
            video.script_path,
            "r",
            encoding="utf-8",
        ) as file:

            script = json.load(file)

        metadata = generate_metadata(
            script,
        )

        os.makedirs(
            "storage/metadata",
            exist_ok=True,
        )

        output = (
            f"storage/metadata/{video.id}.json"
        )

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
        
        video.metadata_path = output

        db.commit()

        return output
