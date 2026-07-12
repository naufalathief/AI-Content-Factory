import argparse

from app.services.video_service import run


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "id",
        type=int,
    )

    args = parser.parse_args()

    output = run(args.id)

    print(f"Video saved to: {output}")


if __name__ == "__main__":
    main()
