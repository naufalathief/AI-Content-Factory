import argparse
import json
import os

from app.db import get_db
from app.models import Video
from app.voice_generator import generate_voice


def main():
    parser = argparse.ArgumentParser(
        description="Generate voice from a script."
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

        if not video.script_path:
            print("Script has not been generated.")
            return

        if not os.path.exists(video.script_path):
            print(f"Script file not found: {video.script_path}")
            return

        with open(video.script_path, "r", encoding="utf-8") as file:
            script = json.load(file)

        text = "\n\n".join([
            script["hook"],
            script["body"],
            script["cta"],
        ])

        os.makedirs("storage/voices", exist_ok=True)

        output_path = f"storage/voices/{video.id}.mp3"

        print("Generating voice...")
        generate_voice(text, output_path)

        video.voice_path = output_path
        video.status = "voiced"

        db.commit()

        print("Voice generated successfully.")
        print(f"Saved to : {output_path}")


if __name__ == "__main__":
    main()
