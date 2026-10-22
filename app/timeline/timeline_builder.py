"""Builds the Remotion timeline from the images and the narration timing.

Every scene's images are placed inside the time window in which that
scene's sentence is actually spoken (from the edge-tts word timings), and
the whole video lasts exactly as long as the voice plus a short tail.
"""

import json
import re
from pathlib import Path

from app import settings
from app.qc import get_audio_duration
from app.schemas import Script
from app.timeline.motion import MotionSelector

_ALNUM = re.compile(r"[^\w]", re.UNICODE)


def _weight(text: str) -> int:
    """Spoken-length proxy that ignores punctuation and spacing."""
    return len(_ALNUM.sub("", text)) or 1


def block_start_times(
    blocks: list[str],
    words: list[dict],
) -> list[float | None]:
    """Start time of every narration block, matched by character position.

    The word stream is matched to the blocks by cumulative character count,
    which survives tokenisation differences such as "well-known" being
    reported as one or two words.
    """

    boundaries: list[int] = []

    total = 0

    for block in blocks:
        total += _weight(block)
        boundaries.append(total)

    starts: list[float | None] = [None] * len(blocks)

    consumed = 0

    block = 0

    for word in words:

        weight = _weight(word["text"])

        middle = consumed + weight / 2

        while block < len(blocks) - 1 and middle > boundaries[block]:
            block += 1

        if starts[block] is None:
            starts[block] = float(word["start"])

        consumed += weight

    return starts


def scene_windows(
    script: Script,
    audio_duration: float,
    words: list[dict] | None,
) -> list[tuple[float, float]]:
    """(start, end) of every scene; the last scene also covers the CTA."""

    blocks = script.narration()

    scene_count = len(script.scenes)

    starts: list[float | None] = (
        block_start_times(blocks, words) if words else [None] * len(blocks)
    )

    # Blocks without timings: place them proportionally to their length.
    total_weight = sum(_weight(block) for block in blocks)

    elapsed = 0.0

    estimated: list[float] = []

    for block in blocks:
        estimated.append(audio_duration * elapsed / total_weight)
        elapsed += _weight(block)

    resolved = [
        estimated[i] if start is None else start
        for i, start in enumerate(starts)
    ]

    resolved[0] = 0.0

    # Keep start times strictly increasing.
    for i in range(1, len(resolved)):
        resolved[i] = max(resolved[i], resolved[i - 1] + 0.05)

    windows = []

    for i in range(scene_count):

        end = (
            resolved[i + 1]
            if i + 1 < scene_count
            else audio_duration
        )

        windows.append((resolved[i], end))

    return windows


class TimelineBuilder:

    WIDTH = settings.VIDEO_WIDTH
    HEIGHT = settings.VIDEO_HEIGHT
    FPS = settings.VIDEO_FPS

    def build(
        self,
        video_id: int,
    ) -> Path:

        image_dir = settings.image_dir(video_id)

        metadata_file = image_dir / "metadata.json"

        if not metadata_file.exists():
            raise FileNotFoundError(metadata_file)

        metadata = json.loads(
            metadata_file.read_text(encoding="utf-8")
        )

        script = Script.from_dict(
            json.loads(
                settings.script_file(video_id).read_text(encoding="utf-8")
            )
        )

        voice = settings.voice_file(video_id)

        words_path = settings.words_file(video_id)

        words = (
            json.loads(words_path.read_text(encoding="utf-8"))
            if words_path.exists()
            else None
        )

        audio_duration = get_audio_duration(str(voice))

        if words:
            audio_duration = max(audio_duration, words[-1]["end"])

        total_duration = audio_duration + settings.VIDEO_TAIL_SECONDS

        windows = scene_windows(script, total_duration, words)

        clips = self.place_clips(
            video_id,
            metadata,
            windows,
            total_duration,
        )

        timeline = {

            "videoId": video_id,

            "width": self.WIDTH,

            "height": self.HEIGHT,

            "fps": self.FPS,

            "totalDuration": round(total_duration, 3),

            "totalFrames": clips[-1]["startFrame"] + clips[-1]["durationFrames"],

            # Paths inside renderer/public (see remotion_assets.sync_assets)
            "audio": f"storage/voices/{video_id}.mp3",

            "subtitle": f"storage/subtitles/{video_id}.srt",

            "clips": clips,

        }

        output = settings.timeline_file(video_id)

        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(
            json.dumps(timeline, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        print("=" * 60)
        print("TIMELINE GENERATED")
        print("=" * 60)
        print(f"Duration : {total_duration:.2f}s ({len(clips)} clips)")
        print(output)

        return output

    def place_clips(
        self,
        video_id: int,
        metadata: list[dict],
        windows: list[tuple[float, float]],
        total_duration: float,
    ) -> list[dict]:

        by_scene: dict[int, list[dict]] = {}

        for item in metadata:
            by_scene.setdefault(int(item["scene"]), []).append(item)

        # Scene numbers in metadata are 1-based; ignore scenes without images
        # by giving their time to the previous scene.
        boundaries: list[tuple[float, dict]] = []

        for number, (start, end) in enumerate(windows, start=1):

            items = by_scene.get(number)

            if not items:
                continue

            weights = [max(float(item["duration"]), 0.1) for item in items]

            total_weight = sum(weights)

            cursor = start

            for item, weight in zip(items, weights):
                boundaries.append((cursor, item))
                cursor += (end - start) * weight / total_weight

        if not boundaries:
            raise RuntimeError(
                f"No images found for video {video_id}."
            )

        selector = MotionSelector(seed=video_id)

        clips = []

        total_frames = round(total_duration * self.FPS)

        for index, (start, item) in enumerate(boundaries):

            # Frame boundaries come from absolute times, so rounding never
            # accumulates into drift between picture and voice.
            start_frame = 0 if index == 0 else round(start * self.FPS)

            end_frame = (
                round(boundaries[index + 1][0] * self.FPS)
                if index + 1 < len(boundaries)
                else total_frames
            )

            duration_frames = max(end_frame - start_frame, 1)

            clips.append(
                {
                    "index": index,
                    "scene": int(item["scene"]),
                    "image": f"storage/images/{video_id}/{item['file']}",
                    "startTime": round(start_frame / self.FPS, 3),
                    "startFrame": start_frame,
                    "duration": round(duration_frames / self.FPS, 3),
                    "durationFrames": duration_frames,
                    "motion": selector.select().to_dict(),
                }
            )

        return clips
