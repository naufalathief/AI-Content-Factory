import json

from app.providers.gemini_client import (
    MODEL_TEXT,
    client,
)

PROMPT_TEMPLATE = """
You are an award-winning YouTube Shorts scriptwriter and cinematic concept artist.

Your task is to generate a HIGH RETENTION YouTube Shorts script AND a cinematic image prompt for every scene.

TOPIC

{topic}

IMPORTANT

- Stay ONLY on the given topic.
- Never change the topic.
- Never introduce unrelated facts.
- Create ONE interesting story only.
- The first sentence MUST hook viewers within 3 seconds.
- Every sentence should naturally lead to the next.
- The last sentence before CTA must deliver the biggest payoff.

SCRIPT RULES

- Native American English.
- 30–45 seconds.
- Around 90–110 words.
- Maximum 6 scenes.
- One sentence per scene.
- Every scene must represent ONE visual moment.

KEYWORD RULES

Generate ONE search keyword suitable for SEO.

STORYBOARD RULES

For EVERY scene generate EXACTLY 3 visuals.

Each visual must contain:

- Ultra realistic
- Cinematic
- Photorealistic
- Vertical composition
- Sharp focus
- No text
- No logo
- No watermark

Each duration must be between 1.3 and 2.0 seconds.

Return ONLY valid JSON.

{{
    "title": "",
    "scenes": [
        {{
            "text": "",
            "keyword": "",
            "visuals": [
                {{
                    "prompt": "",
                    "duration": 1.5
                }},
                {{
                    "prompt": "",
                    "duration": 1.7
                }},
                {{
                    "prompt": "",
                    "duration": 1.8
                }}
            ]
        }}
    ],
    "cta": ""
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


def generate_script(
    topic: str,
) -> dict:

    response = client.models.generate_content(
        model=MODEL_TEXT,
        contents=PROMPT_TEMPLATE.format(
            topic=topic,
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

        return json.loads(text)

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            "Gemini returned invalid JSON."
        ) from exc