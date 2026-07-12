import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)

PROMPT_TEMPLATE = """
Kamu adalah penulis naskah YouTube profesional sekaligus storyboard artist.

Topik:
{topic}

Buat video edukatif berdurasi 3–5 menit.

Aturan:

- Jangan mengarang fakta.
- Gunakan bahasa Indonesia natural.
- Maksimal 5 scene.
- Setiap scene mempunyai keyword visual dalam bahasa Inggris.
- Keyword harus mudah dicari di Pexels.
- Balas HANYA JSON valid.

Format:

{{
  "title": "",
  "scenes": [
    {{
      "text": "",
      "keyword": ""
    }}
  ],
  "cta": ""
}}
"""


def generate_script(topic: str) -> dict:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=PROMPT_TEMPLATE.format(topic=topic),
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text.strip())
