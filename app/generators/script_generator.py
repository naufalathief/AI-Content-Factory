from app import settings
from app.providers.gemini_client import generate_json
from app.schemas import Script

PROMPT_TEMPLATE = """
You are an award-winning YouTube Shorts scriptwriter and cinematic concept artist.

Your task is to generate a HIGH RETENTION YouTube Shorts script AND a cinematic
image prompt for every scene.

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

- Language: {language}.
- 30-45 seconds.
- Around 90-110 words including the CTA.
- Maximum 6 scenes.
- One sentence per scene.
- Every scene must represent ONE visual moment.
- Write numbers the way they should be spoken.

KEYWORD RULES

Generate ONE search keyword per scene suitable for SEO.

STORYBOARD RULES

For EVERY scene generate EXACTLY 3 visuals that follow the sentence in order.

Write each visual prompt in English like a photographer's shot description of
something that could really be photographed. Give every visual ONE clear main
subject; do not stack several subjects or effects into one frame.

- A concrete subject doing a concrete action (who/what, wearing/made of what).
- A specific real location and time of day ("a fishing pier in Maine at dawn",
  not "a beautiful place").
- Shot type and camera angle (close-up, medium shot, low angle, over the
  shoulder, aerial).
- The light that is actually there (overcast daylight, golden hour sun,
  fluorescent office light, campfire).
- One or two small realistic details (dust, condensation, worn edges,
  messy cables) that make it feel real.

Describe only what IS in the frame; never write negatives such as "no hands"
or "without people".

Do NOT use words like "ultra realistic", "8K", "masterpiece", "cinematic",
"epic", "stunning" or "concept art", and never ask for text in the image.
Keep the same people, places and objects consistent across a scene's visuals.

Each visual duration is a relative weight between 1.3 and 2.0. The final
timing is synced to the narration later, so do not try to match seconds.

Leave every scene "duration" at 0.
"""


def generate_script(
    topic: str,
) -> dict:

    script = generate_json(
        PROMPT_TEMPLATE.format(
            topic=topic,
            language=settings.CONTENT_LANGUAGE,
        ),
        Script,
    )

    if not script.scenes:
        raise RuntimeError(
            "Gemini returned a script without scenes."
        )

    for scene in script.scenes:

        scene.duration = 0.0

        if not scene.visuals:
            raise RuntimeError(
                f"Scene has no visuals: {scene.text!r}"
            )

    return script.to_dict()
