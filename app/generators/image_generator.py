import hashlib
import json
import shutil
import time
from pathlib import Path

from PIL import Image
from PIL import ImageOps

from app import settings
from app.image_styles import get_style
from app.providers.gemini_image_provider import generate_image


def build_prompt(
    content_prompt: str,
    style: str,
) -> str:
    # Subject first: image models weigh the start of the prompt most.
    return f"{content_prompt.strip()}, {style}"


class ImageGenerator:

    CACHE_DIR = settings.storage_path("cache", "images")

    WIDTH = settings.VIDEO_WIDTH
    HEIGHT = settings.VIDEO_HEIGHT

    MAX_RETRY = settings.IMAGE_MAX_RETRIES

    def __init__(self):

        self.CACHE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.style = get_style(settings.IMAGE_STYLE)

    def generate(
        self,
        video_id: int,
        script,
    ):

        output_dir = settings.image_dir(video_id)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata = []

        image_index = 1

        total = sum(
            len(scene.visuals)
            for scene in script.scenes
        )

        print("=" * 60)
        print("IMAGE GENERATOR")
        print("=" * 60)

        for scene_number, scene in enumerate(
            script.scenes,
            start=1,
        ):

            for visual_number, visual in enumerate(
                scene.visuals,
                start=1,
            ):

                print(
                    f"[{image_index}/{total}] "
                    f"Scene {scene_number} "
                    f"Visual {visual_number}"
                )

                prompt = build_prompt(
                    visual.prompt,
                    self.style,
                )

                hash_id = hashlib.sha256(
                    prompt.encode()
                ).hexdigest()

                cache = self.CACHE_DIR / f"{hash_id}.png"

                filename = f"{image_index:03}.png"

                output = output_dir / filename

                if cache.exists():

                    print("Cache : HIT")

                else:

                    print("Cache : MISS")

                    self.generate_retry(
                        prompt,
                        cache,
                    )

                shutil.copy2(
                    cache,
                    output,
                )

                metadata.append(
                    {
                        "scene": scene_number,
                        "visual": visual_number,
                        "file": filename,
                        "duration": visual.duration,
                        "width": self.WIDTH,
                        "height": self.HEIGHT,
                        "prompt": prompt,
                        "hash": hash_id,
                    }
                )

                image_index += 1

                print()

        # Written last: its presence marks the step as complete for resume.
        (output_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        print("=" * 60)
        print("DONE")
        print("=" * 60)

    def normalize(
        self,
        image_path: Path,
    ):
        """Crop and resize to exactly 1080x1920 so every frame matches."""

        with Image.open(image_path) as image:

            image.load()

            fitted = ImageOps.fit(
                image.convert("RGB"),
                (self.WIDTH, self.HEIGHT),
                Image.LANCZOS,
                centering=(0.5, 0.45),
            )

        fitted.save(image_path, format="PNG")

    def generate_retry(
        self,
        prompt: str,
        cache_file: Path,
    ):

        tmp = cache_file.with_suffix(".part")

        last_error: Exception | None = None

        for attempt in range(self.MAX_RETRY):

            try:

                print(f"Generate ({attempt + 1}/{self.MAX_RETRY})")

                generate_image(
                    prompt,
                    str(tmp),
                )

                self.verify(tmp)

                self.normalize(tmp)

                # Only a complete, valid image ever lands in the cache.
                tmp.replace(cache_file)

                return

            except Exception as exc:

                last_error = exc

                print(f"Error : {exc}")

                tmp.unlink(missing_ok=True)

                if attempt + 1 < self.MAX_RETRY:
                    time.sleep(2 ** (attempt + 1))

        raise RuntimeError(
            f"Image generation failed after {self.MAX_RETRY} attempts."
        ) from last_error

    def verify(
        self,
        image_path: Path,
    ):

        with Image.open(image_path) as image:

            image.verify()

        with Image.open(image_path) as image:

            width, height = image.size

        if width < 512 or height < 512:

            raise RuntimeError(
                f"Image too small: {width}x{height}."
            )

        return width, height
