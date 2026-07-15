from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from faster_whisper import WhisperModel


MODEL_SIZE = "base"

LANGUAGE = "en"

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

    milliseconds = int(
        round(
            (seconds % 1) * 1000
        )
    )

    total = int(seconds)

    second = total % 60

    total //= 60

    minute = total % 60

    total //= 60

    hour = total

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