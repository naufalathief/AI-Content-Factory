"""Subtitle generation.

Word timings come from edge-tts (saved next to the voice) whenever they are
available. Whisper is only a fallback for audio without timings, so it is
imported lazily and is an optional dependency (requirements-whisper.txt).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from app import settings

if TYPE_CHECKING:
    from faster_whisper import WhisperModel


MODEL_SIZE = "base"

LANGUAGE = settings.WHISPER_LANGUAGE

BEAM_SIZE = 5

MAX_CHARS_PER_LINE = 36
MAX_LINES = 2

MAX_DURATION = 3.5
MIN_DURATION = 1.2

PUNCTUATION = (
    ".",
    "?",
    "!",
    ";",
    ":",
)

_model: WhisperModel | None = None


@dataclass
class Word:

    text: str

    start: float

    end: float


@dataclass
class Caption:

    start: float

    end: float

    text: str


def get_model() -> WhisperModel:

    global _model

    if _model is None:

        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError(
                "No word timings found for this voice and faster-whisper "
                "is not installed. Regenerate the voice, or run "
                "`pip install -r requirements-whisper.txt`."
            ) from exc

        print("=" * 60)
        print("Loading Whisper Model")
        print("=" * 60)

        _model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8",
        )

    return _model


def format_time(seconds: float) -> str:

    # Work in whole milliseconds: rounding the fraction separately could
    # produce ",1000" (e.g. 1.9996 s) and an invalid SRT timestamp.
    total_ms = max(0, int(round(seconds * 1000)))

    total, milliseconds = divmod(total_ms, 1000)

    total, second = divmod(total, 60)

    hour, minute = divmod(total, 60)

    return (
        f"{hour:02}:"
        f"{minute:02}:"
        f"{second:02},"
        f"{milliseconds:03}"
    )

def load_words(
    audio_path: str,
) -> list[Word]:

    model = get_model()

    segments, _ = model.transcribe(

        audio_path,

        language=LANGUAGE,

        beam_size=BEAM_SIZE,

        vad_filter=True,

        word_timestamps=True,

    )

    words: list[Word] = []

    for segment in segments:

        if segment.words is None:
            continue

        for word in segment.words:

            text = word.word.strip()

            if not text:
                continue

            words.append(

                Word(

                    text=text,

                    start=word.start,

                    end=word.end,

                )

            )

    return words


def is_sentence_end(
    word: Word,
) -> bool:

    return word.text.endswith(PUNCTUATION)


def duration(
    words: list[Word],
) -> float:

    return (
        words[-1].end
        - words[0].start
    )


def text_length(
    words: list[Word],
) -> int:

    return len(

        " ".join(

            word.text

            for word in words

        )

    )


def split_lines(
    text: str,
) -> str:

    words = text.split()

    lines: list[str] = []

    current = ""

    for word in words:

        candidate = (

            word

            if not current

            else current + " " + word

        )

        if len(candidate) <= MAX_CHARS_PER_LINE:

            current = candidate

            continue

        lines.append(current)

        current = word

    if current:

        lines.append(current)

    if len(lines) <= MAX_LINES:

        return "\n".join(lines)

    merged: list[str] = []

    while lines:

        if len(lines) == 1:

            merged.append(lines.pop(0))

            break

        first = lines.pop(0)

        second = lines.pop(0)

        merged.append(
            first + " " + second
        )

    return "\n".join(
        merged[:MAX_LINES]
    )


def create_caption(
    words: list[Word],
) -> Caption:

    text = split_lines(

        " ".join(

            word.text

            for word in words

        )

    )

    return Caption(

        start=words[0].start,

        end=words[-1].end,

        text=text,

    )

def segment_words(
    words: list[Word],
) -> list[Caption]:

    captions: list[Caption] = []

    current: list[Word] = []

    for word in words:

        current.append(word)

        current_duration = duration(current)

        current_length = text_length(current)

        should_split = False

        if (
            current_duration >= MAX_DURATION
        ):

            should_split = True

        elif (
            current_length >= (
                MAX_CHARS_PER_LINE
                * MAX_LINES
            )
        ):

            should_split = True

        elif (
            current_duration >= MIN_DURATION
            and is_sentence_end(word)
        ):

            should_split = True

        if should_split:

            captions.append(
                create_caption(current)
            )

            current = []

    if current:

        if (
            captions
            and len(current) <= 3
        ):

            previous = captions.pop()

            merged_words: list[Word] = []

            merged_words.extend(

                Word(
                    text=text,
                    start=previous.start,
                    end=previous.end,
                )

                for text in previous.text.replace(
                    "\n",
                    " ",
                ).split()

            )

            merged_words.extend(current)

            captions.append(
                create_caption(
                    merged_words
                )
            )

        else:

            captions.append(
                create_caption(current)
            )

    balanced: list[Caption] = []

    for caption in captions:

        text = caption.text.replace(
            "\n",
            " ",
        )

        words = text.split()

        if len(words) <= 2:

            if balanced:

                previous = balanced.pop()

                previous = Caption(

                    start=previous.start,

                    end=caption.end,

                    text=(
                        previous.text
                        + " "
                        + text
                    ),

                )

                balanced.append(previous)

            else:

                balanced.append(caption)

            continue

        balanced.append(caption)

    return balanced


def load_timed_words(
    words_path: str | Path,
) -> list[Word]:

    data = json.loads(
        Path(words_path).read_text(encoding="utf-8")
    )

    return [
        Word(
            text=item["text"],
            start=float(item["start"]),
            end=float(item["end"]),
        )
        for item in data
        if item["text"].strip()
    ]


def restore_punctuation(
    words: list[Word],
    text: str,
    max_gap: int = 40,
) -> list[Word]:
    """Map TTS word tokens back onto the original script text.

    edge-tts reports bare words ("Did", "you", "know"). Taking the matching
    span from the script brings back casing and punctuation, which the
    caption splitter needs to break lines at sentence ends.
    """

    lower = text.lower()

    restored: list[Word] = []

    cursor = 0

    remainder = ""

    for word in words:

        token = word.text.strip()

        key = token.lower()

        # A token that is the rest of the previous span ("well-known"
        # spoken as "well" + "known") extends that caption word.
        if restored and remainder and key and key in remainder:

            restored[-1].end = word.end

            remainder = remainder[remainder.index(key) + len(key):]

            continue

        index = lower.find(key, cursor) if key else -1

        if index == -1 or index - cursor > max_gap:

            restored.append(Word(token, word.start, word.end))

            remainder = ""

            continue

        start = index

        while start > cursor and not text[start - 1].isspace():
            start -= 1

        end = index + len(token)

        while end < len(text) and not text[end].isspace():
            end += 1

        restored.append(Word(text[start:end], word.start, word.end))

        remainder = lower[index + len(token):end]

        cursor = end

    return restored


def write_srt(
    captions: list[Caption],
    output_path: str | Path,
) -> None:

    blocks = [
        f"{number}\n"
        f"{format_time(caption.start)} --> {format_time(caption.end)}\n"
        f"{caption.text}\n"
        for number, caption in enumerate(captions, start=1)
    ]

    output = Path(output_path)

    output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(
        "\n".join(blocks),
        encoding="utf-8",
        newline="\n",
    )


def generate_subtitle(
    audio_path: str | Path,
    output_path: str | Path,
    words_path: str | Path | None = None,
    text: str | None = None,
) -> list[Caption]:
    """Build an SRT from TTS word timings, or Whisper as a fallback."""

    if words_path is not None and Path(words_path).exists():

        print("Timing : edge-tts word boundaries")

        words = load_timed_words(words_path)

        if text:
            words = restore_punctuation(words, text)

    else:

        print("Timing : Whisper transcription")

        words = load_words(str(audio_path))

    if not words:
        raise RuntimeError(
            f"No words found for {audio_path}."
        )

    captions = segment_words(words)

    write_srt(captions, output_path)

    return captions
