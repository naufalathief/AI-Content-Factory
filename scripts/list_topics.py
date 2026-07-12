from app.db import get_db
from app.models import Video


def main():
    with get_db() as db:
        videos = (
            db.query(Video)
            .order_by(Video.id)
            .all()
        )

        if not videos:
            print("No topics found.")
            return

        print()

        print("-" * 90)
        print(f"{'ID':<5}{'TOPIC':<65}{'STATUS'}")
        print("-" * 90)

        for video in videos:
            print(
                f"{video.id:<5}"
                f"{video.topic:<65}"
                f"{video.status}"
            )

        print("-" * 90)


if __name__ == "__main__":
    main()
