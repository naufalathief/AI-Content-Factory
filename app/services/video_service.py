import json
import os
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

    render = [
        "remotion",
        "render",
        "src/index.ts",
        "AIContentFactory",
    ]

    if settings.RENDER_MODE == "local":

        command = [
            "npx.cmd" if os.name == "nt" else "npx",
            *render,
            str(output.resolve()),
            f"--props={props}",
        ]

        if settings.REMOTION_BROWSER:
            command.append(f"--browser-executable={settings.REMOTION_BROWSER}")

        cwd = RENDERER_DIR

    else:

        command = [
            "docker",
            "compose",
            "exec",
            "-T",
            settings.RENDERER_SERVICE,
            "npx",
            *render,
            f"/storage/videos/{video_id}.mp4",
            f"--props={props}",
        ]

        cwd = settings.ROOT

    print("=" * 60)
    print("VIDEO RENDER")
    print("=" * 60)
    print(" ".join(command))
    print()

    try:
        result = subprocess.run(command, cwd=cwd)
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"{command[0]} is not available. Use RENDER_MODE=docker with "
            "`docker compose up -d renderer`, or RENDER_MODE=local with "
            "Node.js and `npm ci` in renderer/."
        ) from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"Remotion rendering failed (RENDER_MODE={settings.RENDER_MODE})."
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
