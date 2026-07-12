from app.services.script_service import run as script
from app.services.voice_service import run as voice
from app.services.asset_service import run as asset
from app.services.video_service import run as video
from app.services.subtitle_service import run as subtitle
from app.services.final_video_service import run as final_video
from app.services.metadata_service import run as metadata
from app.services.qc_service import run as qc


def pipeline(video_id: int):
    print("\nGenerating script...")
    script(video_id)

    print("Generating voice...")
    voice(video_id)

    print("Downloading assets...")
    asset(video_id)

    print("Composing video...")
    video(video_id)

    print("Generating subtitle...")
    subtitle(video_id)

    print("Burning subtitle...")
    final_video(video_id)

    print("Generating metadata...")
    metadata(video_id)

    print("Running QC...")
    qc(video_id)


def main():
    while True:

        print()
        print("=" * 40)
        print(" AI CONTENT FACTORY ")
        print("=" * 40)

        print("1. Run Pipeline")
        print("2. QC")
        print("3. Exit")

        choice = input("\nChoose: ")

        if choice == "1":

            video_id = int(input("Video ID: "))

            pipeline(video_id)

        elif choice == "2":

            video_id = int(input("Video ID: "))

            qc(video_id)

        elif choice == "3":

            break

        else:

            print("Invalid menu.")


if __name__ == "__main__":
    main()
