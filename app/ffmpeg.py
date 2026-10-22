"""Locate ffmpeg / ffprobe.

Order: FFMPEG_PATH / FFPROBE_PATH from .env, then the Windows binaries in
tools/ffmpeg/ (not committed, download them there), then the system PATH.
Nothing is checked at import time, so modules that only import this file
keep working on machines without FFmpeg.
"""

import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent

TOOLS = ROOT / "tools" / "ffmpeg"


def _resolve(name: str, env: str) -> str:

    configured = os.getenv(env, "").strip()

    if configured:
        return configured

    if os.name == "nt":

        bundled = TOOLS / f"{name}.exe"

        if bundled.exists():
            return str(bundled)

    return shutil.which(name) or name


FFMPEG = _resolve("ffmpeg", "FFMPEG_PATH")

FFPROBE = _resolve("ffprobe", "FFPROBE_PATH")
