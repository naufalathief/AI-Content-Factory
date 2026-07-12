import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

PROMPT_TEMPLATE = """
Kamu adalah seorang penulis naskah YouTube profesional.

Target penonton:
- Mahasiswa
- Fresh Graduate
- Karyawan
- Orang awam

Tugasmu:

1. Tulis naskah edukatif berdurasi 3–5 menit.
2. Gunakan bahasa Indonesia yang natural.
3. Jangan menggunakan clickbait berlebihan.
4. Jangan mengarang nama AI, perusahaan, fitur, atau produk.
5. Jika tidak yakin suatu informasi benar, jangan masukkan ke dalam script.
6. Prioritaskan informasi yang sudah dikenal luas.
7. Jangan menyebut bahwa kamu adalah AI.
8. Jangan menggunakan Markdown.
9. Jawaban HARUS berupa JSON valid.

Topic:
{topic}

Format:

{{
    "title": "",
    "hook": "",
    "body": "",
    "cta": ""
}}
"""


def generate_script(topic: str) -> dict:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=PROMPT_TEMPLATE.format(
            topic=topic,
        ),
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)
