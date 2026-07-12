import argparse

from app.db import get_db
from app.models import Video


def main():
    parser = argparse.ArgumentParser(
        description="Delete a video topic."
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
            print("Topic not found.")
            return

        db.delete(video)
        db.commit()

        print(f"Topic {args.id} deleted successfully.")


if __name__ == "__main__":
    main()
