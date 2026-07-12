import json
import os
import argparse

from app.db import get_db
from app.models import Video
from app.script_generator import generate_script


def main():
    parser = argparse.ArgumentParser(
        description="Generate YouTube script from a video topic."
    )

    parser.add_argument(
        "id",
        type=int,
        help="Video ID",
    )

    args = parser.parse_args()

    with get_db() as db:
        video = db.get(Video, args.id)

        if video is None:
            print(f"Video with ID {args.id} not found.")
            return

        print(f"Generating script for:")
        print(f"  ID    : {video.id}")
        print(f"  Topic : {video.topic}")
        print()

        script = generate_script(video.topic)

        os.makedirs("storage/scripts", exist_ok=True)

        output_path = f"storage/scripts/{video.id}.json"

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(
                script,
                file,
                ensure_ascii=False,
                indent=4,
            )

        video.script_path = output_path
        video.status = "scripted"

        db.commit()

        print("Script generated successfully.")
        print(f"Saved to : {output_path}")


if __name__ == "__main__":
    main()
