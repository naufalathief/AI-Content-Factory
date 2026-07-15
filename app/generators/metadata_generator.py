import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)

MODEL = "gemini-2.5-flash"

PROMPT = """
Kamu adalah seorang YouTube SEO Specialist.

Berdasarkan data berikut:

Judul:
{title}

Scene:
{body}

CTA:
{cta}

Buat:

1. Judul YouTube maksimal 60 karakter.
2. Deskripsi YouTube sekitar 150–300 kata.
3. Tepat 10 tag YouTube.

Balas HANYA JSON VALID.

Format:

{{
    "title": "",
    "description": "",
    "tags": [
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ]
}}
"""


def clean_json(text: str) -> str:

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_metadata(
    script: dict,
) -> dict:

    body = "\n\n".join(
        scene["text"]
        for scene in script["scenes"]
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT.format(
            title=script["title"],
            body=body,
            cta=script["cta"],
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    text = clean_json(
        response.text,
    )

    try:

        metadata = json.loads(text)

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            "Gemini returned invalid JSON."
        ) from exc

    metadata.setdefault(
        "title",
        script["title"],
    )

    metadata.setdefault(
        "description",
        "",
    )

    metadata.setdefault(
        "tags",
        [],
    )

    metadata["tags"] = metadata["tags"][:10]

    while len(metadata["tags"]) < 10:
        metadata["tags"].append("")

    return metadata