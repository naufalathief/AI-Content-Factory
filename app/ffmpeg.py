from pathlib import Path
import os


ROOT = Path(__file__).resolve().parent.parent

TOOLS = ROOT / "tools" / "ffmpeg"

if os.name == "nt":

    FFMPEG = str(
        TOOLS / "ffmpeg.exe"
    )

    FFPROBE = str(
        TOOLS / "ffprobe.exe"
    )

else:

    FFMPEG = "ffmpeg"

    FFPROBE = "ffprobe"

if os.name == "nt":

    if not Path(FFMPEG).exists():
        raise FileNotFoundError(
            f"FFmpeg not found: {FFMPEG}"
        )

    if not Path(FFPROBE).exists():
        raise FileNotFoundError(
            f"FFprobe not found: {FFPROBE}"
        )