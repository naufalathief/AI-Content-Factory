import argparse

from app.services.asset_service import run as asset
from app.services.script_service import run as script
from app.services.video_service import run as video
from app.services.voice_service import run as voice
from app.services.subtitle_service import run as subtitle


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "id",
        type=int,
    )

    args = parser.parse_args()

    print("[1/5] Generating script...")
    script(args.id)

    print("[2/5] Generating voice...")
    voice(args.id)

    print("[3/5] Downloading assets...")
    asset(args.id)

    print("[4/5] Composing video...")
    video(args.id)

    print("[5/5] Generating subtitle...")
    subtitle(args.id)

    print()
    print("Pipeline completed successfully.")

    print()
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
