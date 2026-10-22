from app import settings
from app.providers.gemini_client import generate_json
from app.schemas import YouTubeMetadata

PROMPT = """
You are a YouTube SEO specialist for YouTube Shorts.

Write everything in this language: {language}.
It must match the language of the video narration below.

Title:
{title}

Narration:
{body}

CTA:
{cta}

Create:

1. A YouTube title of at most 60 characters.
2. A YouTube description of about 150-300 words.
3. Exactly 10 YouTube tags, no "#" sign, no duplicates.
"""

MAX_TITLE = 100  # YouTube's hard limit; the prompt asks for 60.
MAX_TAGS = 10


def generate_metadata(
    script: dict,
) -> dict:

    body = "\n\n".join(
        scene["text"]
        for scene in script["scenes"]
    )

    metadata = generate_json(
        PROMPT.format(
            language=settings.CONTENT_LANGUAGE,
            title=script["title"],
            body=body,
            cta=script["cta"],
        ),
        YouTubeMetadata,
    )

    title = (
        metadata.title.strip()
        or script["title"]
    )[:MAX_TITLE]

    tags: list[str] = []

    for tag in metadata.tags:

        tag = tag.strip().lstrip("#").strip()

        if tag and tag.lower() not in {t.lower() for t in tags}:
            tags.append(tag)

    return {
        "title": title,
        "description": metadata.description.strip(),
        "tags": tags[:MAX_TAGS],
    }
