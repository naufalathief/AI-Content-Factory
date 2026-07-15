from pathlib import Path
import shutil


def sync_assets(video_id: int):

    public = (
        Path("renderer")
        / "public"
        / "storage"
    )

    # Images
    src = (
        Path("storage")
        / "images"
        / str(video_id)
    )

    dst = (
        public
        / "images"
        / str(video_id)
    )

    if dst.exists():
        shutil.rmtree(dst)

    shutil.copytree(src, dst)

    # Voice
    voice_dst = (
        public
        / "voices"
    )

    voice_dst.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        Path("storage")
        / "voices"
        / f"{video_id}.mp3",
        voice_dst
        / f"{video_id}.mp3",
    )

    # Subtitle
    subtitle = (
        Path("storage")
        / "subtitles"
        / f"{video_id}.srt"
    )

    if subtitle.exists():

        subtitle_dst = (
            public
            / "subtitles"
        )

        subtitle_dst.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            subtitle,
            subtitle_dst
            / f"{video_id}.srt",
        )