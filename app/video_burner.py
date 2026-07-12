import os
import subprocess


def burn_subtitle(
    video_path: str,
    subtitle_path: str,
    output_path: str,
):
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            video_path,
            "-vf",
            f"subtitles={subtitle_path}",
            "-c:a",
            "copy",
            output_path,
        ],
        check=True,
    )

    return output_path
