import json
import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)

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

1. Judul YouTube (maksimal 60 karakter)
2. Deskripsi YouTube (150-300 kata)
3. 10 tag YouTube

Balas HANYA JSON valid.

Format:

{{
    "title":"",
    "description":"",
    "tags":[
        "",
        "",
        ""
    ]
}}
"""


def generate_metadata(script: dict):

    body = "\n\n".join(
        scene["text"]
        for scene in script["scenes"]
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=PROMPT.format(
            title=script["title"],
            body=body,
            cta=script["cta"],
        ),
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text.strip())
