"""Central configuration.

Every tunable value lives here and can be overridden from `.env`, so the
generators and services never hard-code models, voices or paths.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str) -> str:
    value = os.getenv(name, "").strip()
    return value or default


ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Storage layout (relative to the project root)
# ---------------------------------------------------------------------------

STORAGE = Path(_env("STORAGE_DIR", "storage"))


def storage_path(*parts: str | int) -> Path:
    return STORAGE.joinpath(*(str(part) for part in parts))


def script_file(video_id: int) -> Path:
    return storage_path("scripts", f"{video_id}.json")


def voice_file(video_id: int) -> Path:
    return storage_path("voices", f"{video_id}.mp3")


def words_file(video_id: int) -> Path:
    """Word-level timings captured while synthesising the voice."""
    return storage_path("voices", f"{video_id}.words.json")


def image_dir(video_id: int) -> Path:
    return storage_path("images", video_id)


def subtitle_file(video_id: int) -> Path:
    return storage_path("subtitles", f"{video_id}.srt")


def timeline_file(video_id: int) -> Path:
    return storage_path("timeline", f"{video_id}.json")


def video_file(video_id: int) -> Path:
    return storage_path("videos", f"{video_id}.mp4")


def final_video_file(video_id: int) -> Path:
    return storage_path("videos", f"{video_id}_final.mp4")


def metadata_file(video_id: int) -> Path:
    return storage_path("metadata", f"{video_id}.json")


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

# Language of the narration, subtitles and YouTube metadata. Keep them in
# one language: an English video with an Indonesian description hurts SEO.
CONTENT_LANGUAGE = _env("CONTENT_LANGUAGE", "Native American English")
WHISPER_LANGUAGE = _env("WHISPER_LANGUAGE", "en")

# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_TEXT_MODEL = _env("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
GEMINI_IMAGE_MODEL = _env("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
GEMINI_MAX_RETRIES = int(_env("GEMINI_MAX_RETRIES", "4"))

# ---------------------------------------------------------------------------
# Voice (edge-tts)
# ---------------------------------------------------------------------------

TTS_VOICE = _env("TTS_VOICE", "en-US-AndrewMultilingualNeural")
TTS_RATE = _env("TTS_RATE", "+0%")

# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

IMAGE_STYLE = _env("IMAGE_STYLE", "default")

# "gemini" (with automatic Pollinations fallback) or "pollinations"
IMAGE_PROVIDER = _env("IMAGE_PROVIDER", "gemini").lower()
IMAGE_MAX_RETRIES = int(_env("IMAGE_MAX_RETRIES", "3"))

# ---------------------------------------------------------------------------
# Video
# ---------------------------------------------------------------------------

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30

# Silence kept after the last word so the CTA is not cut off.
VIDEO_TAIL_SECONDS = float(_env("VIDEO_TAIL_SECONDS", "0.6"))

RENDERER_SERVICE = _env("RENDERER_SERVICE", "renderer")

# "docker": render inside the renderer container (docker compose)
# "local":  run Remotion directly with the Node.js on this machine
RENDER_MODE = _env("RENDER_MODE", "docker").lower()

# Optional Chrome/Chromium binary for local renders (Remotion downloads its
# own headless shell when this is empty).
REMOTION_BROWSER = os.getenv("REMOTION_BROWSER", "").strip()
