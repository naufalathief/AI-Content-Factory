import math
import random
import shutil
import subprocess
from pathlib import Path


# ==========================================
# CONFIG
# ==========================================

WIDTH = 1080
HEIGHT = 1920

FPS = 30

VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"

CRF = 20
PRESET = "medium"

CLIP_DURATION = 2.5

TEMP_FOLDER = "temp"


# ==========================================
# HELPERS
# ==========================================


def run_ffmpeg(command: list[str]):

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )


def run_ffprobe(command: list[str]):

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()


# ==========================================
# AUDIO
# ==========================================


def get_audio_duration(audio_path: str) -> float:

    duration = run_ffprobe(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            audio_path,
        ]
    )

    return float(duration)


# ==========================================
# ASSETS
# ==========================================


def get_asset_files(asset_folder: str) -> list[Path]:

    files = sorted(
        Path(asset_folder).glob("*.mp4")
    )

    if not files:

        raise RuntimeError(
            "No asset videos found."
        )

    return files


def build_timeline(
    assets: list[Path],
    audio_duration: float,
) -> list[Path]:

    clips_needed = math.ceil(
        audio_duration / CLIP_DURATION
    )

    timeline = []

    previous = None

    for _ in range(clips_needed):

        candidates = assets.copy()

        if previous in candidates and len(candidates) > 1:

            candidates.remove(previous)

        clip = random.choice(candidates)

        timeline.append(clip)

        previous = clip

    return timeline

# ==========================================
# VIDEO PREPROCESS
# ==========================================


def prepare_temp_folder():

    temp = Path(TEMP_FOLDER)

    if temp.exists():

        shutil.rmtree(temp)

    temp.mkdir(
        parents=True,
        exist_ok=True,
    )


def preprocess_clip(
    source: Path,
    output: Path,
):

    vf = (
        f"scale={WIDTH}:{HEIGHT}:"
        "force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT},"
        f"fps={FPS}"
    )

    command = [
        "ffmpeg",
        "-y",

        "-stream_loop",
        "-1",

        "-i",
        str(source),

        "-t",
        str(CLIP_DURATION),

        "-vf",
        vf,

        "-an",

        "-c:v",
        VIDEO_CODEC,

        "-preset",
        PRESET,

        "-crf",
        str(CRF),

        str(output),
    ]

    run_ffmpeg(command)


def build_clips(
    timeline: list[Path],
) -> list[Path]:

    prepare_temp_folder()

    clips = []

    for index, asset in enumerate(
        timeline,
        start=1,
    ):

        output = (
            Path(TEMP_FOLDER)
            / f"clip_{index:04}.mp4"
        )

        preprocess_clip(
            asset,
            output,
        )

        clips.append(output)

    return clips


# ==========================================
# CONCAT
# ==========================================


def create_concat_file(
    clips: list[Path],
) -> Path:

    concat = (
        Path(TEMP_FOLDER)
        / "concat.txt"
    )

    with open(
        concat,
        "w",
        encoding="utf-8",
    ) as file:

        for clip in clips:

            file.write(
                f"file '{clip.resolve()}'\n"
            )

    return concat


def concat_video(
    concat_file: Path,
    audio_path: str,
    output_path: str,
):

    command = [

        "ffmpeg",

        "-y",

        "-f",
        "concat",

        "-safe",
        "0",

        "-i",
        str(concat_file),

        "-i",
        audio_path,

        "-map",
        "0:v",

        "-map",
        "1:a",

        "-c:v",
        VIDEO_CODEC,

        "-preset",
        PRESET,

        "-crf",
        str(CRF),

        "-c:a",
        AUDIO_CODEC,

        "-shortest",

        "-movflags",
        "+faststart",

        output_path,
    ]

    run_ffmpeg(command)

# ==========================================
# CLEANUP
# ==========================================


def cleanup():

    temp = Path(TEMP_FOLDER)

    if temp.exists():

        shutil.rmtree(temp)


# ==========================================
# MAIN
# ==========================================


def compose_video(
    audio_path: str,
    asset_folder: str,
    output_path: str,
):

    print("=" * 60)
    print("VIDEO COMPOSER V2")
    print("=" * 60)

    if not Path(audio_path).exists():

        raise FileNotFoundError(audio_path)

    if not Path(asset_folder).exists():

        raise FileNotFoundError(asset_folder)

    audio_duration = get_audio_duration(
        audio_path
    )

    print(
        f"Audio Duration : {audio_duration:.2f}s"
    )

    assets = get_asset_files(
        asset_folder
    )

    print(
        f"Assets Loaded  : {len(assets)}"
    )

    timeline = build_timeline(
        assets,
        audio_duration,
    )

    print(
        f"Timeline Clips : {len(timeline)}"
    )

    clips = build_clips(
        timeline,
    )

    print(
        f"Prepared Clips : {len(clips)}"
    )

    concat = create_concat_file(
        clips,
    )

    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Rendering video...")

    concat_video(
        concat,
        audio_path,
        output_path,
    )

    cleanup()

    print("Done.")
    print(output_path)


# ==========================================
# DEBUG
# ==========================================


if __name__ == "__main__":

    compose_video(
        "storage/voices/1.mp3",
        "storage/assets/1",
        "storage/videos/1.mp4",
    )