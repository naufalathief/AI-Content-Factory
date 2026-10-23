from pathlib import Path

from google.genai import types
from google.genai.errors import APIError

from app import settings
from app.providers.gemini_client import MODEL_IMAGE
from app.providers.gemini_client import get_client
from app.providers.gemini_client import is_quota_error
from app.providers.pollinations_image_provider import (
    generate_image as pollinations_generate_image,
)

ASPECT_RATIO = "9:16"

# After the first quota error in a run, skip Gemini for the remaining
# images instead of failing (and waiting) on every single one.
_quota_exhausted = False


def _generate_gemini(
    prompt: str,
    output: Path,
) -> Path:

    response = get_client().models.generate_content(
        model=MODEL_IMAGE,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=ASPECT_RATIO,
            ),
        ),
    )

    for candidate in response.candidates or []:

        if candidate.content is None:
            continue

        for part in candidate.content.parts or []:

            if part.inline_data and part.inline_data.data:

                output.write_bytes(part.inline_data.data)

                return output

    raise RuntimeError("Gemini returned no image.")


def generate_image(
    prompt: str,
    output_path: str,
):

    global _quota_exhausted

    output = Path(output_path)

    output.parent.mkdir(parents=True, exist_ok=True)

    if settings.IMAGE_PROVIDER not in ("gemini", "pollinations"):
        raise ValueError(
            f"Unknown IMAGE_PROVIDER {settings.IMAGE_PROVIDER!r}; use gemini or pollinations."
        )

    if settings.IMAGE_PROVIDER == "gemini" and not _quota_exhausted:

        try:

            _generate_gemini(prompt, output)

            print("Provider : Gemini")

            return output

        except APIError as exc:

            if not is_quota_error(exc):
                raise

            _quota_exhausted = True

            print("Provider : Gemini")
            print("Status   : Quota Exceeded (skipping Gemini for this run)")

    print("Fallback : Pollinations")

    pollinations_generate_image(
        prompt,
        str(output),
    )

    return output
