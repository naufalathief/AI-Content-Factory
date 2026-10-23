import json
import subprocess
from pathlib import Path

from app import settings
from app.db import get_db
from app.models import Video
from app.services.remotion_assets import sync_assets

RENDERER_DIR = settings.ROOT / "renderer"


def write_props(video_id: int, timeline: dict) -> str:
    """Write the props to a file instead of passing JSON on the command line.

    Long JSON arguments break on Windows quoting and command-length limits.
    Returns the path as seen from inside the renderer container.
    """

    props_dir = RENDERER_DIR / "props"

    props_dir.mkdir(parents=True, exist_ok=True)

    (props_dir / f"{video_id}.json").write_text(
        json.dumps({"timeline": timeline}, ensure_ascii=False),
        encoding="utf-8",
    )

    return f"props/{video_id}.json"


def run(video_id: int):

    timeline_path = settings.timeline_file(video_id)

    if not timeline_path.exists():
        raise FileNotFoundError(timeline_path)

    output = settings.video_file(video_id)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    timeline = json.loads(
        timeline_path.read_text(encoding="utf-8")
    )

    sync_assets(video_id)

    props = write_props(video_id, timeline)

    command = [
        "docker",
        "compose",
        "exec",
        "-T",
        settings.RENDERER_SERVICE,
        "npx",
        "remotion",
        "render",
        "src/index.ts",
        "AIContentFactory",
        f"/storage/videos/{video_id}.mp4",
        f"--props={props}",
    ]

    print("=" * 60)
    print("VIDEO RENDER")
    print("=" * 60)
    print(" ".join(command))
    print()

    try:
        result = subprocess.run(command, cwd=settings.ROOT)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Docker is not available. Start it and run "
            "`docker compose up -d renderer`."
        ) from exc

    if result.returncode != 0:
        raise RuntimeError(
            "Remotion rendering failed. Is the renderer running? "
            "Try `docker compose up -d renderer`."
        )

    if not output.exists():
        raise FileNotFoundError(output)

    with get_db() as db:

        video = db.get(Video, video_id)

        if video is None:
            raise ValueError(f"Video {video_id} not found.")

        video.video_path = str(output)
        video.status = "rendered"

        db.commit()

    print("=" * 60)
    print("VIDEO GENERATED")
    print("=" * 60)

    return str(output)
