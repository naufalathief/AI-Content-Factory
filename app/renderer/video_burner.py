import subprocess
from pathlib import Path

from app.ffmpeg import FFMPEG


FONT_NAME = "Arial"

FONT_SIZE = 9

FONT_COLOR = "&HFFFFFF"

OUTLINE_COLOR = "&H000000"

OUTLINE = 2

SHADOW = 0

MARGIN_V = 60

ALIGNMENT = 2

VIDEO_CODEC = "libx264"

PRESET = "medium"

CRF = "20"


def burn_subtitle(
    video_path: str,
    audio_path: str,
    subtitle_path: str,
    output_path: str,
):
    print("=" * 60)
    print("VIDEO_BURNER V2")
    print("=" * 60)

    video = Path(video_path)
    subtitle = Path(subtitle_path)
    output = Path(output_path)
    audio = Path(audio_path)

    if not video.exists():
        raise FileNotFoundError(video)

    if not subtitle.exists():
        raise FileNotFoundError(subtitle)

    if not audio.exists():
        raise FileNotFoundError(audio)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    subtitle_filter = (
        str(subtitle)
        .replace("\\", "/")
        .replace(":", "\\:")
    )

    style = (
        f"FontName={FONT_NAME},"
        f"FontSize={FONT_SIZE},"
        f"PrimaryColour={FONT_COLOR},"
        f"OutlineColour={OUTLINE_COLOR},"
        f"Outline={OUTLINE},"
        f"Shadow={SHADOW},"
        f"Alignment={ALIGNMENT},"
        f"MarginV={MARGIN_V},"
        "Bold=1"
    )

    command = [

        FFMPEG,

        "-y",

        "-i",
        str(video),

        "-i",
        str(audio),

        "-vf",
        (
            f"subtitles='{subtitle_filter}'"
            f":force_style='{style}'"
        ),

        "-map",
        "0:v:0",

        "-map",
        "1:a:0",

        "-c:v",
        VIDEO_CODEC,

        "-preset",
        PRESET,

        "-crf",
        CRF,

        "-pix_fmt",
        "yuv420p",

        "-c:a",
        "aac",

        "-b:a",
        "192k",

        "-shortest",

        "-movflags",
        "+faststart",

        str(output),

    ]

    print(command)

    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if process.returncode != 0:
        print(process.stderr)
        raise RuntimeError(
            "Failed to burn subtitle."
        )

    print("=" * 60)
    print("FINAL VIDEO CREATED")
    print("=" * 60)
    print(output)