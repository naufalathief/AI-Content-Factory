import argparse

from app.db import get_db
from app.models import Video


def main():
    parser = argparse.ArgumentParser(
        description="Add a new video topic."
    )

    parser.add_argument(
        "topic",
        type=str,
        help="Video topic",
    )

    args = parser.parse_args()

    with get_db() as db:
        video = Video(
            topic=args.topic,
        )

        db.add(video)
        db.commit()
        db.refresh(video)

        print("Topic added successfully.")
        print(f"ID     : {video.id}")
        print(f"Topic  : {video.topic}")
        print(f"Status : {video.status}")


if __name__ == "__main__":
    main()
