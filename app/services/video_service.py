from pathlib import Path
import json
import subprocess

from app.services.remotion_assets import sync_assets


def run(video_id: int):

    timeline = (
        Path("storage")
        / "timeline"
        / f"{video_id}.json"
    )

    if not timeline.exists():
        raise FileNotFoundError(timeline)

    output = (
        Path("storage")
        / "videos"
        / f"{video_id}.mp4"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    props = {

        "timeline": json.loads(

            timeline.read_text(
                encoding="utf-8",
            )

        )

    }

    sync_assets(video_id)

    command = [

        "docker",
        "compose",
        "exec",

        "-T",

        "renderer",

        "npx",

        "remotion",

        "render",

        "src/index.ts",

        "AIContentFactory",

        f"/storage/videos/{video_id}.mp4",

        "--props",

        json.dumps(props),

    ]

    print("=" * 60)
    print("VIDEO RENDER")
    print("=" * 60)

    print("COMMAND")
    print(" ".join(command))
    print()

    result = subprocess.run(command)

    if result.returncode != 0:
        raise RuntimeError(
            "Remotion rendering failed."
        )

    if not output.exists():
        raise FileNotFoundError(output)

    print("=" * 60)
    print("VIDEO GENERATED")
    print("=" * 60)