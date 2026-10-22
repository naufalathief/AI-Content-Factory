"""Text-to-speech with edge-tts.

Besides the MP3, edge-tts reports exactly when each word is spoken. Those
timings drive both the subtitles and the image timeline, so there is no
need to transcribe our own audio with Whisper afterwards.
"""

import asyncio
import json
from pathlib import Path

import edge_tts
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from app import settings

TICKS_PER_SECOND = 10_000_000  # edge-tts offsets are 100 ns ticks


async def _generate(
    text: str,
    output_path: Path,
) -> list[dict]:

    communicate = edge_tts.Communicate(
        text=text,
        voice=settings.TTS_VOICE,
        rate=settings.TTS_RATE,
        boundary="WordBoundary",
    )

    words: list[dict] = []

    tmp = output_path.with_suffix(".part")

    with open(tmp, "wb") as audio:

        async for chunk in communicate.stream():

            if chunk["type"] == "audio":

                audio.write(chunk["data"])

            elif chunk["type"] == "WordBoundary":

                start = chunk["offset"] / TICKS_PER_SECOND
                end = start + chunk["duration"] / TICKS_PER_SECOND

                words.append(
                    {
                        "text": chunk["text"],
                        "start": round(start, 3),
                        "end": round(end, 3),
                    }
                )

    if tmp.stat().st_size == 0:
        tmp.unlink()
        raise RuntimeError("edge-tts returned no audio.")

    tmp.replace(output_path)

    return words


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=20),
    reraise=True,
)
def generate_voice(
    text: str,
    output_path: str | Path,
    words_path: str | Path | None = None,
) -> list[dict]:
    """Write the MP3 and, if `words_path` is given, the word timings JSON."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    words = asyncio.run(
        _generate(
            text=text,
            output_path=output,
        )
    )

    if words_path is not None:

        Path(words_path).write_text(
            json.dumps(words, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    return words
