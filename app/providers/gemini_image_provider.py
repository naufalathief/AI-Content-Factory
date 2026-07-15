from pathlib import Path

from google.genai import types
from google.genai.errors import ClientError

from app.providers.gemini_client import (
    MODEL_IMAGE,
    client,
)
from app.providers.pollinations_image_provider import (
    generate_image as pollinations_generate_image,
)


def generate_image(
    prompt: str,
    output_path: str,
):

    try:

        response = client.models.generate_content(
            model=MODEL_IMAGE,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=[
                    "IMAGE",
                ],
            ),
        )

        image_bytes = None

        for candidate in response.candidates or []:

            if candidate.content is None:
                continue

            for part in candidate.content.parts:

                if (
                    hasattr(part, "inline_data")
                    and part.inline_data
                ):

                    image_bytes = (
                        part.inline_data.data
                    )

                    break

            if image_bytes:
                break

        if image_bytes is None:

            raise RuntimeError(
                "Gemini returned no image."
            )

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_bytes(
            image_bytes,
        )

        print("Provider : Gemini")

        return output

    except ClientError as exc:

        if exc.code != 429:
            raise

        print("Provider : Gemini")
        print("Status   : Quota Exceeded")
        print("Fallback : Pollinations")

        return pollinations_generate_image(
            prompt,
            output_path,
        )