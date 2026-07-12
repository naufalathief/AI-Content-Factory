import os

from faster_whisper import WhisperModel


MODEL = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)


def format_timestamp(seconds: float) -> str:
    milliseconds = int((seconds % 1) * 1000)

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return (
        f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"
    )


def generate_subtitle(
    audio_path: str,
    output_path: str,
):
    segments, _ = MODEL.transcribe(
        audio_path,
        beam_size=5,
        language="id",
    )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        for index, segment in enumerate(
            segments,
            start=1,
        ):

            file.write(f"{index}\n")

            file.write(
                f"{format_timestamp(segment.start)} --> "
                f"{format_timestamp(segment.end)}\n"
            )

            file.write(
                segment.text.strip()
            )

            file.write("\n\n")
