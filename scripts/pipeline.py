"""Run the whole pipeline for one video.

    python -m scripts.pipeline 12               # resume, skip finished steps
    python -m scripts.pipeline 12 --from image  # redo images and everything after
    python -m scripts.pipeline 12 --force       # redo every step
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Callable

from app import settings
from app.services.final_video_service import run as final_video
from app.services.image_service import run as image
from app.services.metadata_service import run as metadata
from app.services.qc_service import run as qc
from app.services.script_service import run as script
from app.services.subtitle_service import run as subtitle
from app.services.timeline_service import run as timeline
from app.services.video_service import run as video
from app.services.voice_service import run as voice


def image_done(video_id: int) -> Path:
    # metadata.json is written last, so it marks a complete image set.
    return settings.image_dir(video_id) / "metadata.json"


# (name, title, service, finished-marker)
STEPS: list[tuple[str, str, Callable[[int], object], Callable[[int], Path]]] = [
    ("script", "Generate Script", script, settings.script_file),
    ("voice", "Generate Voice", voice, settings.voice_file),
    ("image", "Generate Images", image, image_done),
    ("subtitle", "Generate Subtitle", subtitle, settings.subtitle_file),
    ("timeline", "Generate Timeline", timeline, settings.timeline_file),
    ("video", "Render Video", video, settings.video_file),
    ("final", "Burn Subtitle", final_video, settings.final_video_file),
    ("metadata", "Generate Metadata", metadata, settings.metadata_file),
]

STEP_NAMES = [name for name, *_ in STEPS]


def banner(title: str):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="AI Content Factory Pipeline",
    )

    parser.add_argument("id", type=int, help="Video ID")

    parser.add_argument(
        "--from",
        dest="start",
        choices=STEP_NAMES,
        help="Re-run this step and every step after it.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-run every step, ignoring existing outputs.",
    )

    args = parser.parse_args()

    redo_from = 0 if args.force else (
        STEP_NAMES.index(args.start) if args.start else len(STEPS)
    )

    start = time.time()

    banner("AI CONTENT FACTORY")

    total = len(STEPS) + 1

    for number, (name, title, service, done) in enumerate(STEPS, start=1):

        banner(f"[{number}/{total}] {title}")

        marker = done(args.id)

        if number - 1 < redo_from and marker.exists():
            print(f"Status : SKIP ({marker})")
            continue

        step_start = time.time()

        service(args.id)

        print(f"Step time : {time.time() - step_start:.1f}s")

    banner(f"[{total}/{total}] Quality Check")

    if not qc(args.id):
        print("Pipeline failed because QC did not pass.")
        sys.exit(1)

    banner("PIPELINE COMPLETED")

    print(f"Elapsed Time : {time.time() - start:.2f} seconds")
    print()
    print("Outputs")
    print("-" * 60)

    for name, _title, _service, done in STEPS:
        print(f"{name:<12}: {done(args.id)}")

    print("=" * 60)


if __name__ == "__main__":
    main()
