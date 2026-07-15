import argparse
import time

from app.services.final_video_service import run as final_video
from app.services.image_service import run as image
from app.services.metadata_service import run as metadata
from app.services.qc_service import run as qc
from app.services.script_service import run as script
from app.services.subtitle_service import run as subtitle
from app.services.timeline_service import run as timeline
from app.services.video_service import run as video
from app.services.voice_service import run as voice

from tools.pipeline import skip_directory, skip_file


def step(title: str):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="AI Content Factory Pipeline",
    )

    parser.add_argument(
        "id",
        type=int,
        help="Video ID",
    )

    args = parser.parse_args()

    start = time.time()

    print()
    print("=" * 60)
    print("AI CONTENT FACTORY")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. SCRIPT
    # ------------------------------------------------------------------

    step("[1/9] Generate Script")

    if not skip_file(
        f"storage/scripts/{args.id}.json"
    ):
        script(args.id)

    # ------------------------------------------------------------------
    # 2. VOICE
    # ------------------------------------------------------------------

    step("[2/9] Generate Voice")

    if not skip_file(
        f"storage/voices/{args.id}.mp3"
    ):
        voice(args.id)

    # ------------------------------------------------------------------
    # 3. IMAGES
    # ------------------------------------------------------------------

    step("[3/9] Generate Images")

    if not skip_directory(
        f"storage/images/{args.id}"
    ):
        image(args.id)

    # ------------------------------------------------------------------
    # 4. SUBTITLE
    # ------------------------------------------------------------------

    step("[4/9] Generate Subtitle")

    if not skip_file(
        f"storage/subtitles/{args.id}.srt"
    ):
        subtitle(args.id)

    # ------------------------------------------------------------------
    # 5. TIMELINE
    # ------------------------------------------------------------------

    step("[5/9] Generate Timeline")

    if not skip_file(
        f"storage/timeline/{args.id}.json"
    ):
        timeline(args.id)

    # ------------------------------------------------------------------
    # 6. VIDEO
    # ------------------------------------------------------------------

    step("[6/9] Render Video")

    if not skip_file(
        f"storage/videos/{args.id}.mp4"
    ):
        video(args.id)

    # ------------------------------------------------------------------
    # 7. FINAL VIDEO
    # ------------------------------------------------------------------

    step("[7/9] Burn Subtitle")

    if not skip_file(
        f"storage/videos/{args.id}_final.mp4"
    ):
        final_video(args.id)

    # ------------------------------------------------------------------
    # 8. METADATA
    # ------------------------------------------------------------------

    step("[8/9] Generate Metadata")

    if not skip_file(
        f"storage/metadata/{args.id}.json"
    ):
        metadata(args.id)

    # ------------------------------------------------------------------
    # 9. QC
    # ------------------------------------------------------------------

    step("[9/9] Quality Check")

    if not qc(args.id):
        raise RuntimeError(
            "Pipeline failed because QC did not pass."
        )

    elapsed = time.time() - start

    print()
    print("=" * 60)
    print("PIPELINE COMPLETED")
    print("=" * 60)

    print(f"Elapsed Time : {elapsed:.2f} seconds")
    print()

    print("Outputs")
    print("-" * 60)
    print(f"Script       : storage/scripts/{args.id}.json")
    print(f"Voice        : storage/voices/{args.id}.mp3")
    print(f"Images       : storage/images/{args.id}/")
    print(f"Subtitle     : storage/subtitles/{args.id}.srt")
    print(f"Timeline     : storage/timeline/{args.id}.json")
    print(f"Video        : storage/videos/{args.id}.mp4")
    print(f"Final Video  : storage/videos/{args.id}_final.mp4")
    print(f"Metadata     : storage/metadata/{args.id}.json")

    print("=" * 60)


if __name__ == "__main__":
    main()