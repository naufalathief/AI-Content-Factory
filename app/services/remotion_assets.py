import shutil

from app import settings

PUBLIC = settings.ROOT / "renderer" / "public" / "storage"


def sync_assets(video_id: int):
    """Copy the images and voice the renderer needs into renderer/public."""

    src = settings.image_dir(video_id)

    if not src.exists():
        raise FileNotFoundError(src)

    dst = PUBLIC / "images" / str(video_id)

    if dst.exists():
        shutil.rmtree(dst)

    shutil.copytree(src, dst)

    voice = settings.voice_file(video_id)

    if not voice.exists():
        raise FileNotFoundError(voice)

    voice_dst = PUBLIC / "voices"

    voice_dst.mkdir(parents=True, exist_ok=True)

    shutil.copy2(voice, voice_dst / voice.name)
