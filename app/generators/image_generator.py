import hashlib
import json
import shutil
import time
from pathlib import Path

from PIL import Image
from PIL import ImageOps

from app.providers.gemini_image_provider import generate_image
from app.image_prompt_builder import build_prompt
from app.image_styles import DEFAULT_STYLE


class ImageGenerator:

    CACHE_DIR = Path("storage/cache/images")

    MIN_WIDTH = 1024
    MIN_HEIGHT = 1024

    MAX_RETRY = 1

    def __init__(self):

        self.CACHE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate(
        self,
        video_id: int,
        script,
    ):

        output_dir = (
            Path("storage/images")
            / str(video_id)
        )

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
                    DEFAULT_STYLE,
                )

                hash_id = hashlib.sha256(
                    prompt.encode()
                ).hexdigest()

                cache = (
                    self.CACHE_DIR
                    / f"{hash_id}.png"
                )

                filename = (
                    f"{image_index:03}.png"
                )

                output = (
                    output_dir
                    / filename
                )

                if cache.exists():

                    print("Cache : HIT")

                    shutil.copy2(
                        cache,
                        output,
                    )

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

                width, height = self.verify(
                    output,
                )

                metadata.append(

                    {

                        "scene": scene_number,

                        "visual": visual_number,

                        "file": filename,

                        "duration": visual.duration,

                        "width": width,

                        "height": height,

                        "prompt": prompt,

                        "hash": hash_id,

                    }

                )

                image_index += 1

                print()

        with open(

            output_dir / "metadata.json",

            "w",

            encoding="utf-8",

        ) as file:

            json.dump(

                metadata,

                file,

                indent=4,

                ensure_ascii=False,

            )

        print("=" * 60)
        print("DONE")
        print("=" * 60)

    def upscale_if_needed(
        self,
        image_path,
    ):

        image = Image.open(image_path)

        width, height = image.size

        if (
            width >= self.MIN_WIDTH
            and height >= self.MIN_HEIGHT
        ):
            image.close()
            return

        scale = max(
            self.MIN_WIDTH / width,
            self.MIN_HEIGHT / height,
        )

        new_width = int(width * scale)
        new_height = int(height * scale)

        resized = image.resize(
            (new_width, new_height),
            Image.LANCZOS,
        )

        resized.save(image_path)

        image.close()
        resized.close()

    def generate_retry(

        self,

        prompt,

        cache_file,

    ):

        last_error = None

        for attempt in range(

            self.MAX_RETRY,

        ):

            try:

                print(
                    f"Generate ({attempt+1}/{self.MAX_RETRY})"
                )

                generate_image(
                    prompt,
                    str(cache_file),
                )

                self.upscale_if_needed(
                    cache_file,
                )

                self.verify(
                    cache_file,
                )

                return

            except Exception as e:

                last_error = e

                time.sleep(2)

        raise last_error

    def verify(

        self,

        image_path,

    ):

        image = Image.open(
            image_path,
        )

        width, height = image.size

        if width < self.MIN_WIDTH:

            raise RuntimeError(
                "Image width too small."
            )

        if height < self.MIN_HEIGHT:

            raise RuntimeError(
                "Image height too small."
            )

        image.verify()

        image.close()

        return width, height